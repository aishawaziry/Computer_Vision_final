from matplotlib import pyplot as plt
import numpy as np
import os
import cv2
from random import randint


TRAIN_IMG_FOLDER = './static/images/training_data/'

width = 128
height = 128

train_image_names = os.listdir(TRAIN_IMG_FOLDER)
training_tensor = np.ndarray(
    shape=(len(train_image_names), height*width), dtype=np.float64)

for i in range(len(train_image_names)):
    img = cv2.imread((TRAIN_IMG_FOLDER + train_image_names[i]), 0)
    img = cv2.resize(img, dsize=(128, 128))
    training_tensor[i, :] = np.array(img, dtype='float64').flatten()


mean_face = np.mean(training_tensor)

mean_face = np.divide(mean_face, float(len(train_image_names))).flatten()


normalised_training_tensor = training_tensor-mean_face

cov_matrix = np.cov(normalised_training_tensor)

eigenvalues, eigenvectors, = np.linalg.eig(cov_matrix)

sorted_indices = np.argsort(eigenvalues)[::-1]
k = 50
topk_indices = sorted_indices[:k]

reduced_eigenvectors = eigenvectors[:, topk_indices]

proj_data = np.dot(training_tensor.transpose(), reduced_eigenvectors)

proj_data = proj_data.transpose()

w = np.array([np.dot(proj_data, i) for i in normalised_training_tensor])

# print(w)


def Visualization(img_path, t0, train_image_names=train_image_names, proj_data=proj_data, w=w):
    unknown_face = cv2.imread(img_path, 0)
    unknown_face = cv2.resize(unknown_face, dsize=(128, 128))
    img = os.path.basename(img_path)
    unknown_face_vector = np.array(unknown_face, dtype='float64').flatten()
    normalised_uface_vector = np.subtract(unknown_face_vector, mean_face)
    print(t0)
    w_unknown = np.dot(proj_data, normalised_uface_vector)
    diff = w - w_unknown
    norms = np.linalg.norm(diff, axis=1)
    index = np.argmin(norms)
    my_dict = {'output_img_path': '', 'matching_case': '', 'person_name': ''}

    my_dict['output_img_path'] = f'./static/download/face_recognition/{randint(0,9999999999999999)}_face_detection.png'
    if norms[index] < t0:
        match = img.split('_')[0] == train_image_names[index].split('_')[0]
        if match:

            my_dict['matching_case'] = 'Matched'
            name, extension = os.path.splitext(train_image_names[index])
            # plt.title(('Matched:  '+name), color='g')
        else:
            my_dict['matching_case'] = 'False matched'
            # plt.title('False matched', color='r')

        out_img = (cv2.imread(TRAIN_IMG_FOLDER + train_image_names[index]))
        my_dict['person_name'] = train_image_names[index].split('_')[0]
        cv2.imwrite(my_dict['output_img_path'], out_img)

    else:
        my_dict['matching_case'] = 'Unknown face'

        # plt.title('Unknown face', color='r')

    return my_dict


# front_data = Visualization('our_images_test/yasmin_16.jpg',
#                            train_image_names, proj_data, w, t0=2.7e7)

# print(front_data)
