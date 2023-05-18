import numpy as np
import cv2 as cv
from sklearn.cluster import MeanShift, estimate_bandwidth
import numpy as np
import cv2
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import rgb_luv
from random import randint


# =======================Implementation of mean_shift========================================

def mean_shift(X, kernel_bandwidth):
    # initialize centroids
    centroids = X.copy()

    # loop until convergence
    while True:
        # compute distances between each point and each centroid
        nbrs = NearestNeighbors(radius=kernel_bandwidth).fit(centroids)
        distances, indices = nbrs.radius_neighbors(X)

        # compute the mean of each cluster
        new_centroids = []
        for i in range(len(centroids)):
            if len(indices[i]) == 0:
                new_centroids.append(centroids[i])
            else:
                # compute the mean of the points in the cluster
                mean = np.mean(X[indices[i]], axis=0)
                new_centroids.append(mean)

        # check for convergence
        if np.allclose(centroids, new_centroids):
            break

        centroids = new_centroids

    return centroids


def segment(image_path, kernel_bandwidth):
    # read the image path and convert it into the LUV domain
    image = cv.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LUV)

    # reshape image to a 2D array
    pixels = np.reshape(
        image, (image.shape[0] * image.shape[1], image.shape[2]))

    # run mean shift clustering
    centroids = mean_shift(pixels, kernel_bandwidth)

    # assign each pixel to a cluster
    nbrs = NearestNeighbors(n_neighbors=1).fit(centroids)
    distances, indices = nbrs.kneighbors(pixels)

    # reshape the indices back to the original image shape
    indices = np.reshape(indices, (image.shape[0], image.shape[1]))

    # create a segmented image
    segmented = np.zeros_like(image)
    for i in range(len(centroids)):
        segmented[indices == i] = centroids[i]

    return segmented


# # Try code
# # segment image
# segmented = segment('demo_image.jpg', kernel_bandwidth=20)

# # display original and segmented images
# fig, ax = plt.subplots(1, 2, figsize=(10, 5))
# image = cv.imread('demo_image.jpg')
# ax[0].imshow(image)
# ax[0].set_title('Original Image')
# ax[1].imshow(segmented)
# ax[1].set_title('Segmented Image')
# plt.show()


def mean_shift_fast(img_path):
    img = cv.imread(rgb_luv.rgb_luv(img_path))

    # filter to reduce noise
    img = cv.medianBlur(img, 3)

    # flatten the image
    flat_image = img.reshape((-1, 3))
    flat_image = np.float32(flat_image)

    # meanshift
    bandwidth = estimate_bandwidth(flat_image, quantile=.06, n_samples=3000)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, max_iter=800)
    ms.fit(flat_image)
    labeled = ms.labels_

    # get number of segments
    segments = np.unique(labeled)

    # get the average color of each segment
    total = np.zeros((segments.shape[0], 3), dtype=float)
    count = np.zeros(total.shape, dtype=float)
    for i, label in enumerate(labeled):
        total[label] = total[label] + flat_image[i]
        count[label] += 1
    avg = total/count
    avg = np.uint8(avg)

    # cast the labeled image into the corresponding average color
    res = avg[labeled]
    result = res.reshape((img.shape))
    return result


def apply_mean_shift(img_path):
    res_img = mean_shift_fast(img_path)
    img_path = f'./static/download/thresholding/{randint(0,9999999999999999999999999)}_mean_shift.png'
    cv2.imwrite(img_path, res_img)
    return img_path


# result = mean_shift_fast('demo_image.jpg')
# cv.imwrite('mean_result.jpg', result)
# show the result
# cv.imshow('result',result)
# cv.waitKey(0)
# cv.destroyAllWindows()
