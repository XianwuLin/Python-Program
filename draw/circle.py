__author__ = 'Victor'

import cv2
import numpy as np
import pylab as plt
def area_circle(t, data):
    am = 500
    x,y = t[0]*am,t[1]*am
    data *= am
    img = np.zeros((x,y,1),np.uint8)
    for i in data:
        img1 = np.zeros((x,y,1),np.uint8)
        cv2.circle(img1,(i[0],i[1]),i[2],1,-1)
        img = cv2.add(img,img1)

    img0 = []
    area = []
    for i in xrange(3):
        _,dst = cv2.threshold(img, i, 255, cv2.THRESH_BINARY)
        img0.append(cv2.resize(cv2.bitwise_not(dst),(0,0),fx=0.02,fy=0.02))
        contours, hierarchy = cv2.findContours(dst, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        area_t = 0
        for j in contours:
            area_t += cv2.contourArea(j,False)/(am*am)
        area.append(area_t)

    plt.subplot(311),plt.imshow(img0[0],"gray"),plt.title('ALL'),plt.xticks([]),plt.yticks([0])
    plt.subplot(312),plt.imshow(img0[1],"gray"),plt.title('TWO TIMES'),plt.xticks([]),plt.yticks([0])
    plt.subplot(313),plt.imshow(img0[2],"gray"),plt.title('THREE TIMES'),plt.xticks([]),plt.yticks([0])
    plt.show()

    return area


if __name__ == "__main__":
    import csv
    with open ('./data/123.csv','rb') as csv_file:
        data = np.genfromtxt(csv_file, dtype = np.int16, delimiter = ',')
    print area_circle([25,25],data)
