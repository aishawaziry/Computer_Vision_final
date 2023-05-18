import imageio.v3 as iio
import numpy as np
import skimage.color
import skimage.util
import matplotlib.pyplot as plt
import cv2
from scipy.stats import norm
import statistics
from random import randint
import imageio
from PIL import Image
# from profilehooks import profile
import sys
import seaborn as sns


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


def DrawHistogram(img_path):
    image = cv2.imread(img_path)
    # i_mage=rgb2gray(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    flat = image.flatten()
    image = skimage.util.img_as_float(image)
    cv2.imshow('mm', image)
    img_path = f'./static/download/edit/{randint(0,9999999999999999)}_histogram_img.png'
    plt.hist(flat, bins=256, range=(0, 255))
    plt.savefig(img_path)
    return img_path


def Drawdistribution(img):
    image = cv2.imread(img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_path = f'./static/download/edit/{randint(0,9999999999999999)}_distribution_img.png'
    sns.distplot(image, hist=False, kde=True,
                 bins=int(180/5), color='darkblue',
                 hist_kws={'edgecolor': 'black'},
                 kde_kws={'linewidth': 4})
    plt.savefig(img_path)
    plt.show()
    return img_path
