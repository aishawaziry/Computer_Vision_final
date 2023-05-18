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


def rgb2gray(image, mode):
    rgb = []
    r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    if (mode == 0):
        rgb.append(r)
        rgb.append(g)
        rgb.append(b)
        return rgb
    elif (mode == 1):
        return gray


def DrawHistogram(im_array, color):
    img_path = f'./static/download/edit/{randint(0,9999999999999999)}_histogram_img.png'
    plt.hist(im_array, range=(0, 255), linewidth=40, color=color)
    plt.savefig(img_path)
    plt.show()
    return img_path


def rgbmode(im):  # This is what we call
    image = cv2.imread(im)
    rgb = rgb2gray(image, 0)
    rgb_array = []
    # color_list=['r','g','b']
    for i in rgb:
        rgb_channel = np.asarray(i)
        flat = rgb_channel.flatten()
        rgb_array.append(flat)
    return rgb_array
    # return r_path,g_path,b_path


def grayscalemode(img_path):  # This is what we call
    unique, count = np.unique(cv2.imread(img_path, 0), return_counts=True)
    return unique, count


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

# Drawdistribution('./static/download/edit/bl.jpg')


def equalization(img, bin):
    image = cv2.imread(img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    flat = image.flatten()
    # array with size of bins, set to zeros
    hist = np.zeros(bin)
    # loop through pixels and sum up counts of pixels
    for pixel in flat:
        hist[pixel] += 1
    # create our cumulative sum
    hist = iter(hist)
    b = [next(hist)]
    for i in hist:
        b.append(b[-1] + i)
    cs = np.array(b)
    img_new = cs[flat]
    img_new = np.reshape(img_new, image.shape)
    img_path = f'./static/download/edit/{randint(0,9999999999999999)}_equalized_img.png'
    imageio.imwrite(img_path, img_new)
    return img_path

# equalization('./static/download/edit/bl.jpg',256)


def normalization(img):
    img = cv2.imread(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ar = np.array(img).astype(np.float32)
    for i in range(1000):
        mn = np.min(ar)
        mx = np.max(ar)
        norm = (ar - mn) * (1.0 / (mx-mn))
    img_path = f'./static/download/edit/{randint(0,9999999999999999)}_normalized_img.png'
    # cv2.imwrite(img_path,norm )
    imageio.imwrite(img_path, norm)
    return img_path
