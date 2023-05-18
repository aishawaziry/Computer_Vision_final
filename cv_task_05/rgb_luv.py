import cv2
import numpy as np
from random import randint


def rgb_to_luv(r, g, b):
    # Convert RGB values to XYZ color space
    x = r * 0.412453 + g * 0.357580 + b * 0.180423
    y = r * 0.212671 + g * 0.715160 + b * 0.072169
    z = r * 0.019334 + g * 0.119193 + b * 0.950227

    # Convert XYZ values to LUV color space
    x_ref = 0.95047
    y_ref = 1.00000
    z_ref = 1.08883

    u_ref = (4 * x_ref) / (x_ref + (15 * y_ref) + (3 * z_ref))
    v_ref = (9 * y_ref) / (x_ref + (15 * y_ref) + (3 * z_ref))

    u_prime = (4 * x) / (x + (15 * y) + (3 * z))
    v_prime = (9 * y) / (x + (15 * y) + (3 * z))

    l = (116 * ((y / y_ref) ** (1 / 3))) - 16
    u = 13 * l * (u_prime - u_ref)
    v = 13 * l * (v_prime - v_ref)

    return l, u, v


def rgb_luv(img_path):
    rgb_image = cv2.imread(img_path)
    r, g, b = cv2.split(rgb_image)

    l, u, v = rgb_to_luv(r/50, g/13, b/40)

    luv = cv2.merge((l, u, v))
    img_path = f'./static/download/thresholding/{randint(0,9999999999999999)}_luv.png'
    cv2.imwrite(img_path, luv)
    return img_path
