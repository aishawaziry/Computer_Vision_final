import cv2
import numpy as np
from random import randint


def optimal_thresholding(image):
    (height, width) = image.shape
    # initiate both background pixels and foreground elements
    bckGrnd = [image[0][0], image[0][width-1],
               image[height-1][0], image[height-1][width-1]]
    forGrnd = []
    for i in range(height):
        for j in range(width):
            if not ((i == 0 and j == 0) or (i == 0 and j == width-1) or (i == height-1 and j == 0) or (i == height-1 and j == width-1)):
                forGrnd.append(image[i][j])
    # initiate b background and foreground means
    av_bckGrnd = np.mean(bckGrnd)
    av_forGrnd = np.mean(forGrnd)
    thr = (av_bckGrnd+av_forGrnd)/2
    thr_prev = 0
    print(thr)
    while (not (thr_prev == thr)):
        bckGrnd = []
        forGrnd = []
        thr_prev = thr
        for i in range(height):
            for j in range(width):
                if (image[i][j] < thr):
                    bckGrnd.append(image[i][j])
                else:
                    forGrnd.append(image[i][j])
        av_bckGrnd = np.mean(bckGrnd)
        av_forGrnd = np.mean(forGrnd)
        thr = (av_bckGrnd+av_forGrnd)/2
    print(thr)
    return cv2.threshold(image, thr, 255, cv2.THRESH_BINARY)[1]


def apply_optimal_thresholding(img_path):
    thr_img_path = f'./static/download/thresholding/{randint(0,9999999999999)}_optimal_thresholding.png'
    image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    cv2.imwrite(thr_img_path, optimal_thresholding(image))
    return thr_img_path
