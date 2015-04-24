#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   Victor Lin
#   E-mail  :   linxianwusx@gmail.com
#   Date    :   14/12/09 20:39:06
#

import os,sys,cv2

cv2.namedWindow("camera")
det = cv2.CascadeClassifier("./data/haarcascade_frontalface_alt.xml")
cam = cv2.VideoCapture(0)

ret, frame = cam.read() #初始化
while (frame is None):
    ret, frame = cam.read() 

while cam.isOpened():
    ret, frame = cam.read()

    tmp = cv2.cvtColor(frame, cv2.cv.CV_RGB2GRAY)
    objs = det.detectMultiScale(tmp, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
    for rct in objs:
        cv2.rectangle(frame, (rct[0], rct[1]),(rct[0] + rct[2], rct[1] + rct[3]),(0, 0, 255), 2, cv2.CV_AA)

    cv2.imshow("camera", frame)
    if cv2.waitKey(100) == 27:
        cam.release()
        break

cv2.destroyWindow("camera")


