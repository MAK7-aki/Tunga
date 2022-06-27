import cv2
from matplotlib.pyplot import contour
import numpy as np

lower = np.array([130, 0, 220])
upper = np.array([170,255,255])

video = cv2.VideoCapture("rtsp://admin:tunga@2020@192.168.168.64")

while True:
    success,img = video.read()
    img = cv2.resize(img, (640, 480), \
            interpolation = cv2.INTER_LINEAR)
    image = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image,lower,upper)
    
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # print(contours)
    
    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                x,y,w,h = cv2.boundingRect(contour)
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
    
    cv2.imshow("mask",mask)
    cv2.imshow("mask",img)
    
    if cv2.waitKey(1) & 0XFF == ord("q"):
        break