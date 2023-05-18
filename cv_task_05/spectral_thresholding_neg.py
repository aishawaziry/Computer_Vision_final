import numpy as np
import cv2
from random import randint

# Hard Threshold


def hard_thresholding(img, threshold):
    # Compute the 2D Fourier transform of the image
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)

    # Set coefficients below the threshold to zero
    magnitude_spectrum = 20 * np.log(np.abs(fshift))
    print(np.max(magnitude_spectrum))
    magnitude_spectrum[magnitude_spectrum < threshold] = 0
    # Compute the inverse Fourier transform to obtain the filtered image
    fshift[magnitude_spectrum == 0] = 0
    filtered_f = np.fft.ifftshift(fshift)
    filtered_img = np.fft.ifft2(filtered_f)
    filtered_img = np.abs(filtered_img)

    return filtered_img


def apply_hard_thresholding(img_path, threshold):
    print(f'thr = {threshold}')
    img = cv2.imread(img_path, 0)
    # Apply hard thresholding to denoise the image
    filtered_img = hard_thresholding(img, threshold)
    thr_img_path = f'./static/download/thresholding/{randint(0,999999999999)}_hard_threshold.png'
    cv2.imwrite(thr_img_path, filtered_img)
    return thr_img_path


# Soft Threshold
def soft_thresholding(img, threshold, reduction):
    # Compute the 2D Fourier transform of the image
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)

    # Apply soft thresholding to the magnitude spectrum
    magnitude_spectrum = 20 * np.log(np.abs(fshift))
    soft_threshold = np.maximum(magnitude_spectrum - threshold, 0)
    filtered_magnitude_spectrum = magnitude_spectrum - soft_threshold * reduction

    # Compute the inverse Fourier transform to obtain the filtered image
    magnitude_spectrum[magnitude_spectrum == 0] = 1
    filtered_fshift = fshift * filtered_magnitude_spectrum / magnitude_spectrum
    filtered_f = np.fft.ifftshift(filtered_fshift)
    filtered_img = np.fft.ifft2(filtered_f)
    filtered_img = np.abs(filtered_img)
    return filtered_img


def apply_soft_thresholding(img_path, threshold, reduction):
    img = cv2.imread(img_path, 0)
    print(f'thr = {threshold},  red = {reduction}')
    # Apply hard thresholding to denoise the image
    filtered_img = soft_thresholding(img, threshold, reduction)
    thr_img_path = f'./static/download/thresholding/{randint(0,999999999999)}_soft_threshold.png'
    cv2.imwrite(thr_img_path, filtered_img)
    return thr_img_path


# Garrote Threshold
def garrote_thresholding(img, threshold, reduction):
    # Compute the 2D Fourier transform of the image
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)

    # Apply Garrote thresholding to the magnitude spectrum
    magnitude_spectrum = 20 * np.log(np.abs(fshift))
    garrote_threshold = np.maximum(magnitude_spectrum - threshold, 0)
    filtered_magnitude_spectrum = magnitude_spectrum - garrote_threshold * \
        magnitude_spectrum / (magnitude_spectrum + reduction)

    # Compute the inverse Fourier transform to obtain the filtered image
    magnitude_spectrum[magnitude_spectrum == 0] = 1
    filtered_fshift = fshift * filtered_magnitude_spectrum / magnitude_spectrum
    filtered_f = np.fft.ifftshift(filtered_fshift)
    filtered_img = np.fft.ifft2(filtered_f)
    filtered_img = np.abs(filtered_img)
    return filtered_img


def apply_garrote_thresholding(img_path, threshold, reduction):
    print(f'thr = {threshold},  red = {reduction}')
    img = cv2.imread(img_path, 0)
    # Apply hard thresholding to denoise the image
    filtered_img = garrote_thresholding(img, threshold, reduction)
    thr_img_path = f'./static/download/thresholding/{randint(0,999999999999)}_garrote_threshold.png'
    cv2.imwrite(thr_img_path, filtered_img)
    return thr_img_path
