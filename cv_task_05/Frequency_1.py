
import numpy as np
import cv2
from skimage import img_as_ubyte
from matplotlib import pyplot as plt
from random import randint


def global_threshold(img):
    img = cv2.imread(img, 0)

    h = img.shape[0]
    w = img.shape[1]

    img_thres = np.zeros((h, w))
    n_pix = 0
    # loop over the image, pixel by pixel
    for y in range(0, h):
        for x in range(0, w):
            # threshold the pixel
            pixel = img[y, x]
            if pixel < 127:  # because pixel value will be between 0-255.
                n_pix = 0
            else:
                n_pix = pixel
            img_thres[y, x] = n_pix
    img_path = f'./static/download/edit/{randint(0,9999999999999999)}_gloabal_img.png'
    cv2.imwrite(img_path, img_thres)
    return img_path


def local_threshold(img):
    img = cv2.imread(img, 0)
    windowsize_r = 4
    windowsize_c = 4
    sub_img = []
    for r in range(0, img.shape[0] - windowsize_r, windowsize_r):
        for c in range(0, img.shape[1] - windowsize_c, windowsize_c):
            window = img[r:r+windowsize_r, c:c+windowsize_c]
            sub_img.append(window)
    average_list = []
    for iter1 in sub_img:
        height = iter1.shape[0]
        width = iter1.shape[1]
        sum = 0
        average = 0
        for i in range(0, width):
            for j in range(0, height):
                sum += iter1[i][j]
        average = sum/(width * height)
        average_list.append(average)

    new_image = []
    it = 0
    for iter in sub_img:
        height = iter.shape[0]
        width = iter.shape[1]
        for i in range(0, height):
            for j in range(0, width):
                if iter[i][j] > (average_list[it]-2):
                    iter[i][j] = 255
                else:
                    iter[i][j] = 0

        it = it+1
        new_image.append(iter)

    img_path = f'./static/download/edit/{randint(0,9999999999999999)}_local_img.png'
    cv2.imwrite(img_path, img)
    return img_path
