#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   Victor Lin
#   E-mail  :   linxianwusx@gmail.com
#   Date    :   14/12/09 12:17:14
#
import cv2

cv2.namedWindow('Video')
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5, 5))
capture = cv2.VideoCapture(0)
fgbg = cv2.BackgroundSubtractorMOG()
ret, frame = capture.read() 
while (frame is None):
    ret, frame = capture.read() 

while (frame is not None):    
    ret, frame = capture.read()
    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel) 
    contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 

    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) 

    cv2.imshow('Video',frame)

    key = cv2.waitKey(25) 
    if key == ord('q'):  
        break

capture.release()
cv2.destroyWindow('Video')
