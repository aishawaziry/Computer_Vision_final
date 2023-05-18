import cv2
import numpy as np
from random import randint


def otsu_thresholding(img):
    # Calculate histogram and normalize it
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist_norm = hist.ravel() / hist.max()

    # Calculate probabilities of each intensity level
    q = np.cumsum(hist_norm)
    m = np.cumsum(hist_norm * np.arange(256))

    # Calculate inter-class variance for all possible thresholds
    n = len(hist_norm)
    max_var, threshold = 0, 0
    for i in range(1, n):
        w0, w1 = q[i], q[n-1] - q[i]
        if w0 == 0 or w1 == 0:
            continue
        mu0, mu1 = m[i] / w0, (m[n-1] - m[i]) / w1
        var = w0 * w1 * (mu0 - mu1) ** 2
        if var > max_var:
            max_var = var
            threshold = i

    # Apply threshold to the image
    print(threshold)
    return cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)[1]


def apply_otsu_thresholding(img_path):
    img = cv2.imread(img_path, 0)  # read image in grayscale
    thresholded = otsu_thresholding(img)
    th_img_path = f"./static/download/thresholding/{randint(0,99999999999999999999)}_otsu_thresholding.png"
    cv2.imwrite(th_img_path, thresholded)
    return th_img_path
