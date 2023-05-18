import cv2
import numpy as np
from random import randint, random

'''Helping Functions'''


# Convolution Function
def conv(img, krnl):
    '''This function makes 2d convolution as it takes two variable img => 2d array and krnl => array of the kernel
    and return the new array of the new image'''
    krnl_h, krnl_w = len(krnl), len(krnl[0])
    img_h, img_w = img.shape
    img_conv = np.zeros(img.shape)
    for i in range(krnl_h, img_h-krnl_h):
        for j in range(krnl_w, img_w-krnl_w):
            sum = 0
            for m in range(krnl_h):
                for n in range(krnl_w):
                    sum += krnl[m][n]*img[i-krnl_h+m][j-krnl_w+n]
            img_conv[i][j] = sum
    return img_conv


# Average Filter Kernel Generator
def generate_av_kernel(krnl_size):
    '''Generate the average kernel as it takes krnl_size => kernel size and returns kernel => kernel array'''
    kernel = []
    for i in range(krnl_size):
        row = []
        for j in range(krnl_size):
            row.append(1/krnl_size**2)
        kernel.append(row)
    return kernel


'''Noises'''


# Gaussian Noise
def add_gaussian_noise(img_path, var):
    '''This function takes two variable img_path => path of image and var => variance
    and return the path of the generated image'''
    img = cv2.imread(img_path)  # convert image into grayscale
    img = img/255   # normalize the image
    x, y, z = img.shape
    mean = 0
    sigma = np.sqrt(var)
    noise = np.random.normal(loc=mean, scale=sigma, size=(x, y, z))
    img_path = f'./static/download/edit/{randint(0,9999999999999999)}_gaussian_noise_var_{var}_img.png'
    cv2.imwrite(img_path, (noise+img)*255)
    return img_path


# Salt and Pepper Noise
def add_salt_pepper_noise(image, pepper):
    '''This function takes two variable img_path => path of image and pepper => the distribution of balck pixels in filter
    and return the path of the generated image'''
    image = cv2.imread(image)
    output = np.zeros(image.shape, dtype=np.uint8)
    salt = 1 - pepper
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random()
            if rdn < pepper:
                output[i][j] = 0
            elif rdn > salt:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    img_path = f'./static/download/edit/{randint(0,9999999999999999)}_salt_pepper_noise_img.png'
    cv2.imwrite(img_path, output)
    return img_path


# Uniform noise
def add_uniform_noise(img_path, type):
    '''This function takes two variable img_path => path of image and type => type of the image if it is gray or rgb 
    and return the path of the generated image'''
    img = cv2.imread(img_path)
    img = img/255
    if type == 'rgb':
        x, y, z = img.shape
    elif type == 'gray':
        x, y, _ = img.shape
    a = 0
    b = 1.1
    noise = np.zeros(img.shape, dtype=np.uint8)
    for i in range(x):
        for j in range(y):
            noise[i][j] = np.random.uniform(a, b)
    noise_img = img + noise
    noise_img = noise_img*255
    img_path = f'./static/download/edit/{randint(0,9999999999999999)}_uniform_noise_img.png'
    cv2.imwrite(img_path, noise_img)
    return img_path


'''Noise Filters'''


# Median Filter
def add_median_filter(img_path, krnl_size):
    '''This function takes two variable img_path => path of image and krnl_size => kernel size
    and return the path of the generated image'''
    img = cv2.imread(img_path, 0)  # convert image into grayscale
    img_h, img_w = img.shape
    temp_list = []
    indexer = krnl_size//2
    img_final = np.zeros((img_h, img_w))
    for i in range(img_h):
        for j in range(img_w):
            for z in range(krnl_size):
                if i+z-indexer < 0 or i+z-indexer > img_h-1:
                    for c in range(krnl_size):
                        temp_list.append(0)
                else:
                    if j+z-indexer < 0 or j+indexer > img_w-1:
                        temp_list.append(0)
                    else:
                        for k in range(krnl_size):
                            temp_list.append(img[i+z-indexer][j+k-indexer])
            temp_list.sort()
            img_final[i][j] = temp_list[len(temp_list)//2]
            temp_list = []
    img_path = f'./static/download/edit/{randint(0,999999999999999)}_median_filtered_krnl_{krnl_size}_img.png'
    cv2.imwrite(img_path, img_final)
    return img_path


# New Median FIlter
def apply_median_filter(img_path, window_size):
    '''This function takes two variable img_path => path of image and window_size => kernel size
    and return the path of the generated image'''
    img = cv2.imread(img_path, 0)
    filtered_img = np.zeros_like(img)
    padding_size = window_size // 2
    padded_img = np.pad(img, padding_size, mode='symmetric')
    for i in range(padding_size, len(img) + padding_size):
        for j in range(padding_size, len(img[0]) + padding_size):
            window = padded_img[i-padding_size:i+padding_size +
                                1, j-padding_size:j+padding_size+1].flatten()
            median = np.median(window)
            filtered_img[i-padding_size, j-padding_size] = median
    img_path = f'./static/download/edit/{randint(0,999999999999999)}_median_filtered_krnl_{window_size}_img.png'
    cv2.imwrite(img_path, filtered_img)
    return img_path


# Average Filter
def add_average_filter(img_path, krnl_size):
    '''This function takes two variables as it takes img_path => pathof image and krnl_size => size of kernel
    returns the path of generated signal'''
    img = cv2.imread(img_path, 0)  # read image in grayscale
    kernel = generate_av_kernel(krnl_size)
    new_img_path = f'./static/download/edit/{randint(0,9999999999999999)}_average_filter_krnl_{krnl_size}_img.png'
    cv2.imwrite(new_img_path, conv(img, kernel))
    return new_img_path


# New Average Filter
def apply_average_filter(img_path, window_size):
    '''This function takes two variable img_path => path of image and window_size => kernel size
    and return the path of the generated image'''
    img = cv2.imread(img_path, 0)
    filtered_img = np.zeros_like(img)
    padding_size = window_size // 2
    padded_img = np.pad(img, padding_size, mode='symmetric')
    for i in range(padding_size, len(img) + padding_size):
        for j in range(padding_size, len(img[0]) + padding_size):
            window = padded_img[i-padding_size:i+padding_size +
                                1, j-padding_size:j+padding_size+1].flatten()
            median = np.sum(window)/window_size**2
            filtered_img[i-padding_size, j-padding_size] = median
    img_path = f'./static/download/edit/{randint(0,999999999999999)}_average_filtered_krnl_{window_size}_img.png'
    cv2.imwrite(img_path, filtered_img)
    return img_path

# Gaussian Filter


def add_gaussian_filter(img_path):
    img = cv2.imread(img_path, 0)  # read image in grayscale
    kernel = [[1/16, 2/16, 1/16],
              [2/16, 4/16, 2/16],
              [1/16, 2/16, 1/16]]
    new_img_path = f'./static/download/edit/{randint(0,9999999999999999)}_gaussian_filter_img.png'
    cv2.imwrite(new_img_path, conv(img, kernel))
    return new_img_path


'''Edge Detection Filters'''

# Canny Filter


def add_canny_filter(img_path, high_threshold, low_threshold):
    img = cv2.imread(img_path, 0)
    gauss = cv2.GaussianBlur(img, (3, 3), 0)

    Ix = cv2.Sobel(gauss, cv2.CV_64F, 1, 0)
    Iy = cv2.Sobel(gauss, cv2.CV_64F, 0, 1)
    sobel = np.sqrt(np.square(Ix) + np.square(Iy))
    theta = np.arctan2(Iy, Ix)

    M, N = sobel.shape
    Z = np.zeros((M, N), dtype=np.int32)
    angle = theta * 180. / np.pi
    angle[angle < 0] += 180

    for i in range(1, M-1):
        for j in range(1, N-1):
            q = 255
            r = 255

            # angle 0
            if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                q = sobel[i, j+1]
                r = sobel[i, j-1]
            # angle 45
            elif (22.5 <= angle[i, j] < 67.5):
                q = sobel[i+1, j-1]
                r = sobel[i-1, j+1]
            # angle 90
            elif (67.5 <= angle[i, j] < 112.5):
                q = sobel[i+1, j]
                r = sobel[i-1, j]
            # angle 135
            elif (112.5 <= angle[i, j] < 157.5):
                q = sobel[i-1, j-1]
                r = sobel[i+1, j+1]

            if (sobel[i, j] >= q) and (sobel[i, j] >= r):
                Z[i, j] = sobel[i, j]
            else:
                Z[i, j] = 0

    highThreshold = high_threshold
    lowThreshold = low_threshold

    M, N = Z.shape
    res = np.zeros((M, N), dtype=np.int32)

    weak = np.int32(25)
    strong = np.int32(255)

    strong_i, strong_j = np.where(Z >= highThreshold)
    zeros_i, zeros_j = np.where(Z < lowThreshold)

    weak_i, weak_j = np.where((Z <= highThreshold) & (Z >= lowThreshold))

    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak

    strong = 255
    M, N = res.shape
    for i in range(1, M-1):
        for j in range(1, N-1):
            if (res[i, j] == weak):
                try:
                    if ((res[i+1, j-1] == strong) or (res[i+1, j] == strong) or (res[i+1, j+1] == strong)
                        or (res[i, j-1] == strong) or (res[i, j+1] == strong)
                            or (res[i-1, j-1] == strong) or (res[i-1, j] == strong) or (res[i-1, j+1] == strong)):
                        res[i, j] = strong
                    else:
                        res[i, j] = 0
                except IndexError as e:
                    pass

    img_path = f'./static/download/edit/{randint(0,9999999999999999)}_canny_img.png'
    cv2.imwrite(img_path, res)

    return img_path


# Prewitt Edge Detection Filter
def add_prewitt_filter(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img_x = conv(img, [[-1, 0, 1],
                       [-1, 0, 1],
                       [-1, 0, 1]])
    img_y = conv(img, [[-1, -1, -1],
                       [0, 0, 0],
                       [1, 1, 1]])
    prewitt_img_path = f'./static/download/edit/{randint(0,3333333333655)}_prewitt_img.png'
    cv2.imwrite(prewitt_img_path, img_x+img_y)
    return prewitt_img_path


# Roberts Edge Detection Filter
def add_roberts_filter(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img_x = conv(img, [[1, 0],
                       [0, -1]])
    img_y = conv(img, [[0, 1],
                       [-1, 0]])
    roberts_img_path = f'./static/download/edit/{randint(0,3333333333655)}_roberts_img.png'
    cv2.imwrite(roberts_img_path, img_x+img_y)
    return roberts_img_path


# Sobel Edge Detection Filter
def add_sobel_filter(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img_x = conv(img, [[-1, 0, 1],
                       [-2, 0, 2],
                       [-1, 0, 1]])
    img_y = conv(img, [[-1, -2, -1],
                       [0, 0, 0],
                       [1, 2, 1]])
    sobel_img_path = f'./static/download/edit/{randint(0,3333333333655)}_sobel_img.png'
    cv2.imwrite(sobel_img_path, img_x+img_y)
    return sobel_img_path


def grayscale_mode(img_path):
    unique, count = np.unique(cv2.imread(img_path, 0), return_counts=True)
    return [unique.tolist(), count.tolist()]


def get_unique(arr):
    unique, count = np.unique(arr, return_counts=True)
    return [unique.tolist(), count.tolist()]


def get_rgb(img_path):
    b, g, r = cv2.split(cv2.imread(img_path))
    r_scale = get_unique(r)
    g_scale = get_unique(g)
    b_scale = get_unique(b)
    return [r_scale, g_scale, b_scale]


def get_gray(img_path):
    return get_unique(cv2.imread(img_path, 0))


def convert_to_gray_scale(img_path):
    img = cv2.imread(img_path, 0)
    gray_img_path = f'./static/download/edit/{randint(0,3333333333655)}_gray_img.png'
    cv2.imwrite(gray_img_path, img)
    return gray_img_path


def get_cumulative_curve(img_path):
    list_x = []
    for i in range(256):
        list_x.append(i)
    image = cv2.imread(img_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    flat = image.flatten()
    # array with size of bins, set to zeros
    hist = np.zeros(256)
    # loop through pixels and sum up counts of pixels
    for pixel in flat:
        hist[pixel] += 1
    # create our cumulative sum
    hist = iter(hist)
    b = [next(hist)]
    for i in hist:
        b.append(b[-1] + i)
    cs = np.array(b)

    return [list_x, cs.tolist()]


# Testing Counting Function unique img
def search_index(index, img):
    count = 0
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i][j] == index:
                count += 1
    return count


def unique_img(img):
    unique_arr = np.zeros(256)
    for i in range(len(unique_arr)):
        unique_arr[i] = search_index(i, img)
    return unique_arr
