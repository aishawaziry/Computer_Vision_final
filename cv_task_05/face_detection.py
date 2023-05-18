import cv2
from random import randint
from PIL import Image


def face_detection(img_path,minNeighbor,minsize):
    haar_data=cv2.CascadeClassifier('./static/xmls/haarcascade_frontalface_default.xml')
    img = cv2.imread(img_path)
    faces=haar_data.detectMultiScale(img,minNeighbors=minNeighbor,minSize=[minsize,minsize])
    for x,y,h,w in faces:
        cv2.rectangle(img,(x,y),(x+w,(y+h)),(255,0,0),3)
       
    img_path = f'./static/download/face_detection/{randint(0,9999999999999999)}_face_detection.png'

    cv2.imwrite(img_path,img) 
    return img_path