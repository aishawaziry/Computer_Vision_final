import cv2
import numpy as np
from random import randint


def euclidean_distance(point1, point2):

    return np.linalg.norm(np.array(point1) - np.array(point2))


def clusters_distance(cluster1, cluster2):
    for point1 in cluster1:
        for point2 in cluster2:
            return min(euclidean_distance(point1, point2))


def clusters_distance_2(cluster1, cluster2):

    cluster1_center = np.average(cluster1, axis=0)
    cluster2_center = np.average(cluster2, axis=0)
    return euclidean_distance(cluster1_center, cluster2_center)


class AgglomerativeClusteringClass:

    def __init__(self, k, initial_k):
        self.k = k
        self.initial_k = initial_k

    def initial_clusters(self, points):

        groups = {}
        d = int(256 / (self.initial_k))
        for i in range(self.initial_k):
            j = i * d
            groups[(j, j, j)] = []
        for i, p in enumerate(points):
            group = min(groups.keys(), key=lambda c: euclidean_distance(p, c))
            groups[group].append(p)
        return [g for g in groups.values() if len(g) > 0]

    def fit(self, points):

        # initially, assign each point to a distinct cluster
        self.clusters_list = self.initial_clusters(points)

        while len(self.clusters_list) > self.k:

            # Find the closest pair of clusters
            cluster1, cluster2 = min([(c1, c2) for i, c1 in enumerate(self.clusters_list) for c2 in self.clusters_list[:i]],
                                     key=lambda c: clusters_distance_2(c[0], c[1]))

            # Remove the two clusters from the clusters list
            self.clusters_list = [
                c for c in self.clusters_list if c != cluster1 and c != cluster2]

            # collect the two clusters
            merged_cluster = cluster1 + cluster2

            # Add the clusters list
            self.clusters_list.append(merged_cluster)

        self.cluster = {}
        for cl_num, cl in enumerate(self.clusters_list):
            for point in cl:
                self.cluster[tuple(point)] = cl_num

        self.centers = {}
        for cl_num, cl in enumerate(self.clusters_list):
            self.centers[cl_num] = np.average(cl, axis=0)

    def predict_cluster(self, point):

        return self.cluster[tuple(point)]

    def predict_center(self, point):

        point_cluster_num = self.predict_cluster(point)
        center = self.centers[point_cluster_num]
        return center


def agglomerative_clustering(img_path, n_clusters, initial_k):
    img = cv2.imread(img_path)[:, :, ::-1]
    img_shaped = img.reshape((-1, 3))
    print(f'N clust= {n_clusters}, K initial={initial_k}')
    Agglo = AgglomerativeClusteringClass(n_clusters, initial_k)

    Agglo.fit(img_shaped)

    new_img = [[Agglo.predict_center(list(pixel))
                for pixel in row] for row in img]
    new_img = np.array(new_img, np.uint8)
    new_img = new_img[:, :, ::-1]
    img_path = f'./static/download/thresholding/{randint(0,9999999999999999)}_AgglomerativeClustering.png'

    cv2.imwrite(img_path, new_img)
    return img_path

# img = agglomerative_clustering("images\sample.jpg",4,20)
