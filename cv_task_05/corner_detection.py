import cv2
import numpy as np
from random import randint


def em_harris_corner(img_path):
    image = cv2.imread(img_path)
    operatedImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # modify the data type
    # setting to 32-bit floating point
    operatedImage = np.float32(operatedImage)
    # apply the cv2.cornerHarris method
    # to detect the corners with appropriate
    # values as input parameters
    dest = cv2.cornerHarris(operatedImage, 2, 5, 0.04)
    # Results are marked through the dilated corners
    dest = cv2.dilate(dest, None)
    # Reverting back to the original image,
    # with optimal threshold value
    image[dest > 0.01 * dest.max()] = [0, 0, 255]
    # the window showing output image with corners
    img_path = f'./static/download/edit/{randint(0,999999999999999999)}_harris_corner_detection_img.png'
    cv2.imwrite(img_path, image)
    return img_path


def add_harris_corner(img_path):
    # Load the image and convert to grayscale
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Define the parameters for the algorithm
    block_size = 2
    ksize = 3
    k = 0.04
    # Compute the derivatives using the Sobel operator
    Ix = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=ksize)
    Iy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=ksize)
    # Compute the elements of the Harris matrix
    Ix2 = Ix ** 2
    Iy2 = Iy ** 2
    Ixy = Ix * Iy
    # Initialize the corner response image
    corner_response = np.zeros_like(gray)
    # Compute the corner response for each pixel
    for y in range(block_size, gray.shape[0] - block_size):
        for x in range(block_size, gray.shape[1] - block_size):
            # Compute the sum of the elements of the Harris matrix in the neighborhood
            Sxx = np.sum(Ix2[y-block_size:y+block_size +
                         1, x-block_size:x+block_size+1])
            Syy = np.sum(Iy2[y-block_size:y+block_size +
                         1, x-block_size:x+block_size+1])
            Sxy = np.sum(Ixy[y-block_size:y+block_size +
                         1, x-block_size:x+block_size+1])
            # Compute the determinant and trace of the Harris matrix
            det = Sxx * Syy
            trace = Sxx + Syy
            # Compute the corner response using the Harris response equation and the k parameter
            corner_response[y, x] = det - k * trace ** 2
    # Normalize the corner response image
    corner_response = cv2.normalize(
        corner_response, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    img[corner_response > 0.01*corner_response.max()] = [0, 0, 255]
    img_path = f'./static/download/edit/{randint(0,999999999999999999)}_harris_corner_detection_img.png'
    cv2.imwrite(img_path, img)
    return img_path


def apply_harris_corner(img_dir, window_size, k, threshold):
    img = cv2.imread(img_dir)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gaussian = cv2.GaussianBlur(gray, (3, 3), 0)
    height = img.shape[0]  # .shape[0] outputs height
    # .shape[1] outputs width .shape[2] outputs color channels of image
    width = img.shape[1]
    matrix_R = np.zeros((height, width))

    #   Step 1 - Calculate the x and y image derivatives (dx and dy)
    dx = cv2.Sobel(img_gaussian, cv2.CV_64F, 1, 0, ksize=3)
    dy = cv2.Sobel(img_gaussian, cv2.CV_64F, 0, 1, ksize=3)

    #   Step 2 - Calculate product and second derivatives (dx2, dy2 and dxy)
    dx2 = np.square(dx)
    dy2 = np.square(dy)
    dxy = dx*dy

    offset = int(window_size / 2)
    #   Step 3 - Calculate the sum of two products of the derivatives for each pixel (Sx2, Sy2 and Sxy)
    for y in range(offset, height-offset):
        for x in range(offset, width-offset):
            Sx2 = np.sum(dx2[y-offset:y+1+offset, x-offset:x+1+offset])
            Sy2 = np.sum(dy2[y-offset:y+1+offset, x-offset:x+1+offset])
            Sxy = np.sum(dxy[y-offset:y+1+offset, x-offset:x+1+offset])

            #   Step 4 - Define the matrix H(x,y)=[[Sx2,Sxy],[Sxy,Sy2]]
            H = np.array([[Sx2, Sxy], [Sxy, Sy2]])

            #   Step 5 - Calculate the response function ( R=det(H)-k(Trace(H))^2 )
            det = np.linalg.det(H)
            tr = np.matrix.trace(H)
            R = det-k*(tr**2)
            matrix_R[y-offset, x-offset] = R

    #   Step 6 - Apply a threshold
    cv2.normalize(matrix_R, matrix_R, 0, 1, cv2.NORM_MINMAX)
    for y in range(offset, height-offset):
        for x in range(offset, width-offset):
            value = matrix_R[y, x]
            if value > threshold:
                cv2.circle(img, (x, y), 1, (0, 0, 255))
    img_path = f'./static/download/edit/{randint(0,999999999999999999)}_harris_corner_detection_thr_{threshold}_img.png'
    cv2.imwrite(img_path, img)
    return img_path
