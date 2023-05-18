from flask import Flask, render_template, request, make_response, jsonify
import base64
import os
import numpy as np
from random import randint
import filter_fun as fn
import Histograms as hs
import Frequency_2 as fr2
import Frequency_1 as fr1
import corner_detection as crn
import ActiveContour as ct
import Hough as hf
import cv2
import ellipse_detection as ed
import ssd_ncc
import otsu_thresholding as ots
import optimal_thresholding as opt
import mean_local_thresholding as mlt
import spectral_thresholding_neg as spt
import image_segmentation as im_sg
import agglomerative_clustering as ag_cl
import k_means as kms
import mean_shift as mns
import rgb_luv as luv
import spectral_thresholding as spc_thr
import face_recognition as fcrg
import face_detection as fcd
import roc
app = Flask(__name__)


def modify_path(path):
    new_path = './'+'/'.join(path.split('/')[3::])
    return new_path


def handle_filter(img_path, filter_name):
    new_path_img = ''
    if filter_name == 'gaussian_noise':
        new_path_img = fn.add_gaussian_noise(img_path, 0.05)
    elif filter_name == 'average_filter':
        new_path_img = fn.apply_average_filter(img_path, 9)
    elif filter_name == 'gaussian_filter':
        new_path_img = fn.add_gaussian_filter(img_path)
    elif filter_name == 'median_filter':
        new_path_img = fn.apply_median_filter(img_path, 9)
    elif filter_name == 'uniform_noise':
        new_path_img = fn.add_uniform_noise(img_path, 'rgb')
    elif filter_name == 'salt_Papper_noise':
        new_path_img = fn.add_salt_pepper_noise(img_path, 0.05)
    elif filter_name == 'sobel_filter':
        new_path_img = fn.add_sobel_filter(img_path)
    elif filter_name == 'prewitt_filter':
        new_path_img = fn.add_prewitt_filter(img_path)
    elif filter_name == 'roberts_filter':
        new_path_img = fn.add_roberts_filter(img_path)
    elif filter_name == 'canny_filter':
        new_path_img = fn.add_canny_filter(img_path, 100, 100)
    elif filter_name == "low_pass_filter":
        new_path_img = hs.LPF_rgb(img_path)
    elif filter_name == "high_pass_filter":
        new_path_img = hs.HPF_rgb(img_path)
    elif filter_name == "normalizer":
        new_path_img = fr2.normalization(img_path)
    elif filter_name == "equalizer":
        new_path_img = fr2.equalization(img_path, 256)
    elif filter_name == "gloabal_thresholding":
        new_path_img = fr1.global_threshold(img_path)
    elif filter_name == "local_thresholding":
        new_path_img = fr1.local_threshold(img_path)
    elif filter_name == "convert_to_grayscale":
        new_path_img = fn.convert_to_gray_scale(img_path)
    elif filter_name == "harris_corner":
        new_path_img = crn.apply_harris_corner(img_path, 5, 0.04, 0.2)
    return new_path_img


def save(img_path):
    list_img = os.listdir('./static/upload/hf')
    for img in list_img:
        path = './static/upload/hf/'+img
        os.remove(path)

    img_path_new = f'./static/upload/hf/{randint(0,999999999999999999)}.png'
    cv2.imwrite(img_path_new, cv2.imread(img_path))
    return img_path_new


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/recieve_hybrid', methods=['GET', 'POST'])
def get_hybrid_imgs():
    if request.method == 'POST':
        list_imgs_d = os.listdir('./static/download/hybrid')
        list_imgs_up = os.listdir('./static/upload/hybrid')
        for img in list_imgs_d:
            path = './static/download/hybrid/'+img
            os.remove(path)
        for img in list_imgs_up:
            path = './static/upload/hybrid/'+img
            os.remove(path)

        req = request.get_json()
        upld_img1 = base64.b64decode(req["img1"].split(',')[1])
        upld_img2 = base64.b64decode(req["img2"].split(',')[1])

        upld_img1_file = './static/upload/hybrid/upld_hyb_img1.png'
        upld_img2_file = './static/upload/hybrid/upld_hyb_img2.png'

        with open(upld_img1_file, 'wb') as f:
            f.write(upld_img1)
        with open(upld_img2_file, 'wb') as f:
            f.write(upld_img2)

        res = make_response(
            jsonify({'Message': "Transformation has been done successfully", "img": hs.hybrid_rgb(upld_img1_file, upld_img2_file)}), 200)
        return res


@app.route('/recieve_img', methods=['GET', 'POST'])
def get_img():
    if request.method == 'POST':
        list_imgs_d = os.listdir('./static/download/edit')
        list_imgs_up = os.listdir('./static/upload/edit')
        for img in list_imgs_d:
            path = './static/download/edit/'+img
            os.remove(path)
        for img in list_imgs_up:
            path = './static/upload/edit/'+img
            os.remove(path)

        req = request.get_json()
        upld_img = base64.b64decode(req["img"].split(',')[1])

        upld_img_file = f'./static/upload/edit/{randint(0,99999999999999999)}_upld_edit_img.png'

        with open(upld_img_file, 'wb') as f:
            f.write(upld_img)

        res = make_response(
            jsonify({'Message': "Transformation has been done successfully", 'img': upld_img_file}), 200)
        return res


@app.route('/apply_filter', methods=['POST', 'GET'])
def apply_filter():
    if request.method == 'POST':
        req = request.get_json()
        print(modify_path(req['img']))
        res = make_response(
            jsonify({'Message': "Transformation has been done successfully", 'img': handle_filter(modify_path(req['img']), req['value'])}), 200)
        return res


@app.route('/recieve_histogram', methods=['POST', 'GET'])
def recieve_histogram():
    if request.method == 'POST':
        req = request.get_json()
        values = fn.grayscale_mode(modify_path(req['img']))
        res = make_response(
            jsonify({'Message': "Transformation has been done successfully", 'values': values}), 200)
        return res


@app.route('/recieve_distribution_curve', methods=['POST', 'GET'])
def recive_distribution_curve():
    if request.method == 'POST':
        req = request.get_json()
        values = fn.grayscale_mode(modify_path(req['img']))
        res = make_response(
            jsonify({'Message': "Transformation has been done successfully", 'values': values}), 200)
        return res


@app.route('/recieve_rgb', methods=['POST', 'GET'])
def recive_rgba_gray():
    if request.method == 'POST':
        req = request.get_json()
        rgb = fn.get_rgb(modify_path(req['img']))
        gray = fn.get_gray(modify_path(req['img']))
        if req['value'] == 'grayscale':
            values = gray
        elif req['value'] == 'redscale':
            values = rgb[0]
        elif req['value'] == 'greenscale':
            values = rgb[1]
        elif req['value'] == 'bluescale':
            values = rgb[2]
        res = make_response(
            jsonify({'Message': "Transformation has been done successfully", 'values': values}), 200)
        return res


@app.route('/recieve_cml_curve', methods=['POST', 'GET'])
def recieve_cml():
    if request.method == 'POST':
        req = request.get_json()
        cml_value = fn.get_cumulative_curve(modify_path(req['img']))
        res = make_response(
            jsonify({'Message': "Transformation has been done successfully", 'values': cml_value}), 200)
        return res


@app.route('/active_contour', methods=['POST', 'GET'])
def recieve_active_contour():
    if request.method == 'POST':
        list_imgs_d = os.listdir('./static/download/ac_hf')
        for img in list_imgs_d:
            path = './static/download/ac_hf/'+img
            os.remove(path)
        req = request.get_json()
        active_contour_img = ct.active_contour(
            modify_path(req['img']), 20, 0.3, 500, 30, 30, 350)
        print(active_contour_img)
        res = make_response(
            jsonify({'Message': "Transformation has been done successfully", 'img': active_contour_img}), 200)
        return res


@app.route('/active_hough', methods=['POST', 'GET'])
def recieve_hough():
    if request.method == 'POST':
        list_imgs_d = os.listdir('./static/download/hf')
        for img in list_imgs_d:
            path = './static/download/hf/'+img
            os.remove(path)
        req = request.get_json()
        print(modify_path(req['img']))
        img_path = save(modify_path(req['img']))
        if req['type'] == "detect_line":
            hough_img = hf.houghLine(
                img_path, int(req['threshold']))
        elif req['type'] == "detect_circle":
            hough_img = hf.detectCircles(img_path, threshold=int(req['threshold']), region=50, radius=[
                                         int(req['xradiaus']), int(req['yradius'])])
        elif req['type'] == "detect_ellipse":
            hough_img = ed.ellipse_detection(img_path)
        res = make_response(
            jsonify({'Message': "Transformation has been done successfully", 'img': hough_img}), 200)
        return res


@app.route('/ssd_ncc_recive', methods=['POST', 'GET'])
def ssd_ncc_recive():
    if request.method == 'POST':
        list_imgs_d = os.listdir('./static/download/ssd')
        for img in list_imgs_d:
            path = './static/download/ssd/'+img
            os.remove(path)

        req = request.get_json()
        upld_img1 = base64.b64decode(req["img1"].split(',')[1])
        upld_img2 = base64.b64decode(req["img2"].split(',')[1])

        threshold = float(req['threshold'])
        mode = req['method']

        upld_img1_file = './static/upload/sdd/ssd_ncc_img1.png'
        upld_img2_file = './static/upload/sdd/ssd_ncc_img2.png'

        with open(upld_img1_file, 'wb') as f:
            f.write(upld_img1)
        with open(upld_img2_file, 'wb') as f:
            f.write(upld_img2)
        mode_time, img_rslt, sift_time = ssd_ncc.feature_matching(
            upld_img1_file, upld_img2_file, threshold, mode)
        res = make_response(
            jsonify({'Message': "Transformation has been done successfully", "img": img_rslt, 'mode': mode, 'mode_time': np.round(mode_time, 2), 'sift_time': np.round(sift_time, 2)}), 200)
        return res


@app.route('/ts4_recive_new', methods=['POST', 'GET'])
def apply_threshold():
    if request.method == 'POST':
        th_imgs_list_up = os.listdir('./static/upload/thresholding')
        for img in th_imgs_list_up:
            path = './static/upload/thresholding/'+img
            os.remove(path)

        th_imgs_list_dn = os.listdir('./static/download/thresholding')
        for img in th_imgs_list_dn:
            path = './static/download/thresholding/'+img
            os.remove(path)

        req = request.get_json()
        upld_img = base64.b64decode(req["orImg"].split(',')[1])

        upld_img_file = f'./static/upload/thresholding/{randint(0,99999999999999999)}_ts4_up.png'

        with open(upld_img_file, 'wb') as f:
            f.write(upld_img)

        dwn_img_path = upld_img_file
        if (req["thType"] == "otsu_thresholding"):
            dwn_img_path = ots.apply_otsu_thresholding(upld_img_file)
        elif (req["thType"] == "optimal_thresholding"):
            dwn_img_path = opt.apply_optimal_thresholding(upld_img_file)
        elif (req["thType"] == "spectral_thresholding_mod"):
            dwn_img_path = spc_thr.apply_spectral_thresholding(upld_img_file)
        elif (req["thType"] == "mean_shift_segmentation"):
            dwn_img_path = mns.apply_mean_shift(upld_img_file)
        elif (req["thType"] == "rgb_luv"):
            dwn_img_path = luv.rgb_luv(upld_img_file)
        elif (req["thType"] == "local_thresholding"):
            dwn_img_path = mlt.apply_mean_local_threshold(upld_img_file, int(
                req["lclBlockSize"]), int(req["lclThresholdWeight"]))
        elif (req["thType"] == "region_growing"):
            dwn_img_path = im_sg.region_growing(upld_img_file, int(
                req["lclBlockSize"]), int(req["lclThresholdWeight"]))
        elif (req["thType"] == "agglomerative_clustring"):
            dwn_img_path = ag_cl.agglomerative_clustering(upld_img_file, int(
                req["lclBlockSize"]), int(req["lclThresholdWeight"]))
        elif (req["thType"] == "k_mean_segmentation"):
            dwn_img_path = kms.apply_kmeans_segmentation(upld_img_file, int(
                req["lclBlockSize"]), int(req["lclThresholdWeight"]))
        elif (req["thType"] == "spectral_thresholding"):
            if (req["mode"] == "hard_thresholding"):
                dwn_img_path = spt.apply_hard_thresholding(
                    upld_img_file, float(req["threshold"]))
            elif (req["mode"] == "soft_thresholding"):
                dwn_img_path = spt.apply_soft_thresholding(
                    upld_img_file, float(req["threshold"]), float(req["reduction"]))
            elif (req["mode"] == "garrote_thresholding"):
                dwn_img_path = spt.apply_garrote_thresholding(
                    upld_img_file, float(req["threshold"]), float(req["reduction"]))

        res = make_response(
            jsonify({'Message': "Transformation has been done successfully", "img": dwn_img_path}), 200)
        return res


@app.route('/face_recognition', methods=['POST', 'GET'])
def face_recognition():
    if request.method == 'POST':
        th_imgs_list_up = os.listdir('./static/upload/face_recognition/')
        for img in th_imgs_list_up:
            path = './static/upload/face_recognition/'+img
            os.remove(path)

        th_imgs_list_dn = os.listdir('./static/download/face_recognition/')
        for img in th_imgs_list_dn:
            path = './static/download/face_recognition/'+img
            os.remove(path)

        req = request.get_json()
        upld_img = base64.b64decode(req["img"].split(',')[1])

        upld_img_file = f'./static/upload/face_recognition/{req["name"]}'

        with open(upld_img_file, 'wb') as f:
            f.write(upld_img)

        data = roc.Visualization(upld_img_file, int(req['thr']))
        img = data['output_img_path']
        stat = data['matching_case']
        prs_name = data['person_name']
        # roc_img = roc.roc(int(req['thr']))
        res = make_response(
            jsonify({'Message': "Transformation has been done successfully", "img": img, "stat": stat, "prs_name": prs_name,}), 200)
        return res


@app.route('/face_detection', methods=['POST', 'GET'])
def face_detection():
    if request.method == 'POST':
        th_imgs_list_up = os.listdir('./static/upload/face_detection/')
        for img in th_imgs_list_up:
            path = './static/upload/face_detection/'+img
            os.remove(path)

        th_imgs_list_dn = os.listdir('./static/download/face_detection/')
        for img in th_imgs_list_dn:
            path = './static/download/face_detection/'+img
            os.remove(path)

        req = request.get_json()
        upld_img = base64.b64decode(req["img"].split(',')[1])

        upld_img_file = f'./static/upload/face_detection/{req["name"]}'

        with open(upld_img_file, 'wb') as f:
            f.write(upld_img)

        img = fcd.face_detection(upld_img_file,12,5)
        res = make_response(
            jsonify({'Message': "Transformation has been done successfully", "img": img}), 200)
        return res


if __name__ == "__main__":
    app.run()
