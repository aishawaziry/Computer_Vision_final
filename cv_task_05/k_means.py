import cv2
from scipy.spatial import distance_matrix
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
from random import randint
import rgb_luv
np.seterr(divide='ignore', invalid='ignore')


class KMeans():
    def __init__(self, n_clus, max_iter):

        self.n_clus = n_clus  # Number of clusters
        self.centroids = None
        self.X = None
        self.clusters = None
        self.max_iter = max_iter

    def getCentroids(self):
        return self.centroids

    def getClusters(self):
        return self.clusters

    def fit(self, X, init_state=None):
        Npts, Ndim = X.shape
        self.X = X

        if init_state is None:
            X_max, X_min = np.max(X), np.min(X)
            self.centroids = np.random.uniform(
                low=X_min, high=X_max, size=(self.n_clus, Ndim))
        else:
            self.centroids = init_state

        for i in range(self.max_iter):

            diff = cdist(X, self.centroids, metric="euclidean")
            self.clusters = np.argmin(diff, axis=1)

            for i in range(self.n_clus):
                self.centroids[i] = np.mean(
                    X[np.where(self.clusters == i)], axis=0)


def kmeans_segmentation(img_path, n_clus, max_iter):
    print("K Means")
    image = cv2.imread(rgb_luv.rgb_luv(img_path))  # Read image
    X = image.reshape((-1, 3))  # Reshape to (Npts, Ndim = 3)
    X = np.float32(X)

    # Call the kmeans class
    km = KMeans(n_clus, max_iter)
    km.fit(X)
    centers = km.getCentroids()
    clusters = km.getClusters()

    segmented_image = centers[clusters]

    segmented_image = segmented_image.reshape((image.shape))
    return segmented_image


def apply_kmeans_segmentation(img_path, n_clus, max_iter):
    result_arr = kmeans_segmentation(img_path, n_clus, max_iter)
    print(f"k = {n_clus}, max = {max_iter}")
    img_path = f'./static/download/thresholding/{randint(0,99999999999999999999999999999)}_kmeans_segmentation.png'
    cv2.imwrite(img_path, result_arr)
    return img_path


# input k and maximum index
# result_arr = kmeans_segmentation('images\eiffle.png', 3, 50)
# cv2.imwrite('kmeans_result.jpg',segmented_image)
