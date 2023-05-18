import cv2
import numpy as np
import time
from random import randint
import SIFTimplementation


def drawMatches(img1, kp1, img2, kp2, matches):

    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1, rows2]), cols1+cols2, 3), dtype='uint8')

    out[:rows1, :cols1, :] = np.dstack([img1, img1, img1])

    out[:rows2, cols1:cols1+cols2, :] = np.dstack([img2, img2, img2])

    for count, mat in enumerate(matches):

        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        (x1, y1) = kp1[img1_idx].pt
        (x2, y2) = kp2[img2_idx].pt

        cv2.circle(out, (int(x1), int(y1)), 4,
                   ((count+2)*10, count*25, count*30), 1)
        cv2.circle(out, (int(x2)+cols1, int(y2)), 4,
                   ((2+count)*10, count*25, count*30), 1)

        cv2.line(out, (int(x1), int(y1)), (int(x2)+cols1, int(y2)),
                 ((2+count)*10, count*25, count*30), 1)

    img_path = f'./static/download/ssd/{randint(0,9999999999999999)}_feature.png'
    cv2.imwrite(img_path, out)
    return img_path


def ncc_matching(keypoints_1, keypoints_2, desc1, desc2, threshold):

    matches = []

    for i in range(len(desc1)):
        for j in range(len(desc2)):
            out1_norm = (desc1[i] - np.mean(desc1[i])) / (np.std(desc1[i]))
            out2_norm = (desc2[j] - np.mean(desc2[j])) / (np.std(desc2[j]))
            corr_vector = np.multiply(out1_norm, out2_norm)
            corr = float(np.mean(corr_vector))
            if corr > threshold:
                matches.append([i, j, corr])

    final = []
    for i in range(len(matches)):
        dis = np.linalg.norm(np.array(
            keypoints_1[matches[i][0]].pt) - np.array(keypoints_2[matches[i][1]].pt))
        final.append(cv2.DMatch(matches[i][0], matches[i][1], dis))
    return final


def ssd_matching(keypoints_1, keypoints_2, desc1, desc2, threshold):

    matches = []
    for i in range(len(desc1)):
        for j in range(len(desc2)):
            ssd = np.sum(np.square(desc1[i]-desc2[j]))
            if ssd < threshold:
                matches.append([i, j, ssd])
    final = []
    for i in range(len(matches)):
        dis = np.linalg.norm(np.array(
            keypoints_1[matches[i][0]].pt) - np.array(keypoints_2[matches[i][1]].pt))
        final.append(cv2.DMatch(matches[i][0], matches[i][1], dis))
    return final


def feature_matching(img_path1, img_path2, threshold, mode):

    # read images
    img1 = cv2.imread(img_path1, 0)
    img2 = cv2.imread(img_path2, 0)

    # sift = cv2.SIFT_create()
    # keypoints_1, descriptors_1 = sift.detectAndCompute(img1, None)
    # keypoints_2, descriptors_2 = sift.detectAndCompute(img2, None)

    # sift = cv2.SIFT_create()
    # keypoints_1, descriptors_1 = sift.detectAndCompute(img1, None)
    # keypoints_2, descriptors_2 = sift.detectAndCompute(img2, None)
    sift1 = SIFTimplementation.SIFT(img_path1)
    keypoints_1, descriptors_1 = sift1.computeKeypointsAndDescriptors()
    sift_time_st = time.time()
    sift2 = SIFTimplementation.SIFT(img_path2)
    keypoints_2, descriptors_2 = sift2.computeKeypointsAndDescriptors()
    sift_time_end = time.time()
    sift_total_time = sift_time_end-sift_time_st
    if mode == 'ssd':
        print("ssd")
        start = time.time()
        matches = ssd_matching(keypoints_1, keypoints_2,
                               descriptors_1, descriptors_2, threshold)
        end = time.time()
        total_time = end-start

    elif mode == 'ncc':
        print("ncc")
        start = time.time()
        matches = ncc_matching(keypoints_1, keypoints_2,
                               descriptors_1, descriptors_2, threshold)
        end = time.time()
        total_time = end-start
    new_path = drawMatches(img1, keypoints_1, img2, keypoints_2, matches[:10])
    print(total_time)
    return total_time, new_path, sift_total_time


# feature_matching("images\cat256.jpg", "images\cat512.png", 0.93, "ncc")
