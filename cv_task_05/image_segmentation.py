import cv2
import numpy as np
from random import randint


def check_points(img, seed):

    row, col = np.shape(img)

    region_grow = np.zeros((row+1, col+1))
    # seeds point should be inverted since seed[1] is the x coordinate and seed[0] is the y coordinate
    swap = [seed[1], seed[0]]
    region_grow[swap[0]][swap[1]] = 255
    region_points = [[swap[0], swap[1]]]
    # the window of 8 pixels that we take around each point
    x_k = [-1, 0, 1, -1, 1, -1, 0, 1]
    y_k = [-1, -1, -1, 0, 0, 1, 1, 1]
    c = 0
    while len(region_points) > 0:

        if c == 0:
            check_point = region_points.pop(0)
            i = check_point[0]
            j = check_point[1]

        intensity = img[i][j]
        low = intensity - 8
        high = intensity + 8

        for k in range(8):
            if region_grow[i + x_k[k]][j + y_k[k]] != 255:
                try:
                    if low < img[i + x_k[k]][j + y_k[k]] < high:
                        region_grow[i + x_k[k]][j + y_k[k]] = 255
                        region_points.append([i + x_k[k], j + y_k[k]])
                    else:
                        region_grow[i + x_k[k]][j + y_k[k]] = 0
                except IndexError:
                    continue
        # we remove the point the was checked and make i and j takes the values for the next point
        check_point = region_points.pop(0)
        i = check_point[0]
        j = check_point[1]
        c = c + 1
    return region_grow


def region_growing(img_path, seedx, seedy):
    print(f'seedX={seedx}, seedY={seedy}')
    img = cv2.imread(img_path, 0)
    seed_points = [seedx, seedy]
    region_grow_image = check_points(img, seed_points)
    img_path = f'./static/download/thresholding/{randint(0,9999999999999999)}_Region_growing.png'
    cv2.imwrite(img_path, region_grow_image)
    return img_path
