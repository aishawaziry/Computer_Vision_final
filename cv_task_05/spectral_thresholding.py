import numpy as np
from random import randint
import cv2


def spectral_threshold(img):
    # Compute the histogram of the image
    hist, _ = np.histogram(img, 256, [0, 256])
    # Calculate the mean of the entire image
    mean = np.sum(np.arange(256) * hist) / float(img.size)
    # Initialize variables for the optimal threshold values and the maximum variance
    optimal_high = 0
    optimal_low = 0
    max_variance = 0
    # Loop over all possible threshold values, select ones with maximum variance between modes
    for high in range(0, 256):
        for low in range(0, high):
            w0 = np.sum(hist[0:low])
            if w0 == 0:
                continue
            mean0 = np.sum(np.arange(0, low) * hist[0:low]) / float(w0)
            # Calculate the weight and mean of the low pixels
            w1 = np.sum(hist[low:high])
            if w1 == 0:
                continue
            mean1 = np.sum(np.arange(low, high) * hist[low:high]) / float(w1)
            # Calculate the weight and mean of the high pixels
            w2 = np.sum(hist[high:])
            if w2 == 0:
                continue
            mean2 = np.sum(np.arange(high, 256) * hist[high:]) / float(w2)

            # Calculate the beween-class variance
            variance = w0 * (mean0 - mean) * 2 + w1 * \
                (mean1 - mean) * 2 + w2 * (mean2 - mean) ** 2
            # Update the optimal threshold values if the variance is greater than the maximum variance
            if variance > max_variance:
                max_variance = variance
                optimal_high = high
                optimal_low = low
    # Apply thresholding to the input image using the optimal threshold values
    binary = np.zeros(img.shape, dtype=np.uint8)
    binary[img < optimal_low] = 0
    binary[(img >= optimal_low) & (img < optimal_high)] = 128
    binary[img >= optimal_high] = 255
    return binary


def apply_spectral_thresholding(img):
    img_path = f'./static/download/thresholding/{randint(0,999999999999999)}_spectral_threshold.png'
    cv2.imwrite(img_path, spectral_threshold(cv2.imread(img, 0)))
    return img_path
