import cv2
import numpy as np
from random import randint


def mean_local_threshold(img, block_size, constant_c):
    neighborhood_size = block_size
    C = constant_c
    output = np.zeros_like(img)
    # Iterate over each pixel in the image
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # Compute the local threshold for the current pixel
            neighborhood = img[max(i-neighborhood_size//2, 0):min(i+neighborhood_size//2+1, img.shape[0]),
                               max(j-neighborhood_size//2, 0):min(j+neighborhood_size//2+1, img.shape[1])]
            threshold = np.mean(neighborhood) - C
            if img[i, j] > threshold:
                output[i, j] = 255
    return output


def apply_mean_local_threshold(img_path, block_size, constant_c):
    img = cv2.imread(img_path, 0)
    print(block_size)
    print(constant_c)
    thr_img_path = f'./static/download/thresholding/{randint(0,99999999999999999)}_mean_local_thresholding.png'
    cv2.imwrite(thr_img_path, mean_local_threshold(
        img, block_size, constant_c))
    return thr_img_path
