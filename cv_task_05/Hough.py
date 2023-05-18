import cv2
import numpy as np
import math
import imageio
from random import randint
import matplotlib.pyplot as plt
from collections import defaultdict


def hough_peaks(H, num_peaks, nhood_size=3):
    # loop through number of peaks to identify
    indices = []
    H1 = np.copy(H)
    for i in range(num_peaks):
        idx = np.argmax(H1)  # find argmax in flattened array
        H1_idx = np.unravel_index(idx, H1.shape)  # remap to shape of H
        indices.append(H1_idx)

        # surpass indices in neighborhood
        idx_y, idx_x = H1_idx  # first separate x, y indexes from argmax(H)
        # if idx_x is too close to the edges choose appropriate values
        if (idx_x - (nhood_size / 2)) < 0:
            min_x = 0
        else:
            min_x = idx_x - (nhood_size / 2)
        if (idx_x + (nhood_size / 2) + 1) > H.shape[1]:
            max_x = H.shape[1]
        else:
            max_x = idx_x + (nhood_size / 2) + 1

        # if idx_y is too close to the edges choose appropriate values
        if (idx_y - (nhood_size / 2)) < 0:
            min_y = 0
        else:
            min_y = idx_y - (nhood_size / 2)
        if (idx_y + (nhood_size / 2) + 1) > H.shape[0]:
            max_y = H.shape[0]
        else:
            max_y = idx_y + (nhood_size / 2) + 1

        # bound each index by the neighborhood size and set all values to 0
        for x in range(int(min_x), int(max_x)):
            for y in range(int(min_y), int(max_y)):
                # remove neighborhoods in H1
                H1[y, x] = 0

                # highlight peaks in original H
                if x == min_x or x == (max_x - 1):
                    H[y, x] = 255
                if y == min_y or y == (max_y - 1):
                    H[y, x] = 255

    # return the indices and the original Hough space with selected points
    return indices, H


def hough_lines_draw(img, indices, rhos, thetas):
    rho = []
    for i in range(len(indices)):
        # reverse engineer lines from rhos and thetas
        # if(indices[i][0]<783):
        rho = rhos[int(indices[i][0])]
        # if(indices[i][1]<180):
        theta = thetas[int(indices[i][1])]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        # these are then scaled so that the lines go off the edges of the image
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    img_path = f'./static/download/edit/{randint(0,9999999999999999)}_line_detection.png'
    # img_path = f'./static/download/edit/_line_detection.png'
    cv2.imwrite(img_path, img)
    return img_path


def houghLine(img, peaksnum):
    # reding the photo and applying canny edge detection on it
    image = cv2.imread(img)
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (5, 5), 0)
    edge = cv2.Canny(blur, 50, 150)
    # Get image dimensions
    # y for rows and x for columns
    Ny = edge.shape[0]
    Nx = edge.shape[1]

    # Max diatance is diagonal one
    Maxdist = int(np.round(np.sqrt(Nx**2 + Ny ** 2)))
    # Theta in range from -90 to 90 degrees
    thetas = np.deg2rad(np.arange(-90, 90))
    # Range of radius
    rhos = np.linspace(-Maxdist, Maxdist, 2*Maxdist)
    accumulator = np.zeros((2 * Maxdist, len(thetas)))
    for y in range(Ny):
        for x in range(Nx):
            # Check if it is an edge pixel
            #  NB: y -> rows , x -> columns
            if edge[y, x] > 0:
                # Map edge pixel to hough space
                for k in range(len(thetas)):
                    # Calculate space parameter
                    r = x*np.cos(thetas[k]) + y * np.sin(thetas[k])
                    # Update the accumulator
                    # N.B: r has value -max to max
                    # map r to its idx 0 : 2*max
                    accumulator[int(r) + Maxdist, k] += 1
    # getting the indicies of peaks to draw it on the photo
    indicies, acci = hough_peaks(accumulator, peaksnum)
    print('done')
    img_path = hough_lines_draw(image, indicies, rhos, thetas)
    return img_path

# 56 for cairo-building3.jpg
# 10 for xogame.png
# 24 for lines2.jpg
# 20 for images (1).png
# houghLine('lines2.jpg', 24)


# ===================================================================================================================

def detectCircles(input_img, threshold, region, radius=None):
    imgread = cv2.imread(input_img)
    img = cv2.cvtColor(imgread, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (5, 5), 1.5)
    img = cv2.Canny(img, 100, 200)
    (M, N) = img.shape
    if radius == None:
        R_max = np.max((M, N))
        R_min = 3
    else:
        [R_max, R_min] = radius

    print(radius)
    print(input_img)
    R = R_max - R_min
    # Initializing accumulator array.
    # Accumulator array is a 3 dimensional array with the dimensions representing
    # the radius, X coordinate and Y coordinate resectively.
    # Also appending a padding of 2 times R_max to overcome the problems of overflow
    A = np.zeros((R_max, M+2*R_max, N+2*R_max))
    B = np.zeros((R_max, M+2*R_max, N+2*R_max))

    # Precomputing all angles to increase the speed of the algorithm
    theta = np.arange(0, 360)*np.pi/180
    edges = np.argwhere(img[:, :])  # Extracting all edge coordinates
    for val in range(R):
        r = R_min+val
        # Creating a Circle Blueprint
        bprint = np.zeros((2*(r+1), 2*(r+1)))
        (m, n) = (r+1, r+1)  # Finding out the center of the blueprint
        for angle in theta:
            x = int(np.round(r*np.cos(angle)))
            y = int(np.round(r*np.sin(angle)))
            bprint[m+x, n+y] = 1
        constant = np.argwhere(bprint).shape[0]
        for x, y in edges:  # For each edge coordinates
            # Centering the blueprint circle over the edges
            # and updating the accumulator array
            X = [x-m+R_max, x+m+R_max]  # Computing the extreme X values
            Y = [y-n+R_max, y+n+R_max]  # Computing the extreme Y values
            A[r, X[0]:X[1], Y[0]:Y[1]] += bprint
        A[r][A[r] < threshold*constant/r] = 0

    for r, x, y in np.argwhere(A):
        temp = A[r-region:r+region, x-region:x+region, y-region:y+region]
        try:
            p, a, b = np.unravel_index(np.argmax(temp), temp.shape)
        except:
            continue
        B[r+(p-region), x+(a-region), y+(b-region)] = 1
    print('done')
    img_path = displayCircles(B[:, R_max:-R_max, R_max:-R_max], imgread)
    return img_path


def displayCircles(A, img):
    circleCoordinates = np.argwhere(A)  # Extracting the circle information
    for r, x, y in circleCoordinates:
        cv2.circle(img, (y, x), r, color=(0, 255, 0), thickness=2)
    img_path = f'./static/download/edit/{randint(0,9999999999999999)}_circle_detection.png'
    # img_path = f'./static/download/edit/{randint(0,100000000000000000000)}_circle_detection.png'
    cv2.imwrite(img_path, img)
    return img_path

# detectCircles('planets.jpg', threshold=15, region=50,radius=[150, 100]) # for planets
# detectCircles('coin2.jpg', threshold=15, region=50,radius=[100, 40])  # for coin2
