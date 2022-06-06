import cv2
import numpy as np

tracker = cv2.TrackerMOSSE_create()
video = cv2.VideoCapture("rtsp://admin:tunga@2020@192.168.168.64")

ok,frame=video.read()
frame = cv2.resize(frame, (640, 480))
bbox = cv2.selectROI(frame)
ok = tracker.init(frame,bbox)
while True:
   ok,frame=video.read()
   frame = cv2.resize(frame, (640, 480), \
            interpolation = cv2.INTER_LINEAR)
   if not ok:
        break
   ok,bbox=tracker.update(frame)
   if ok:
        (x,y,w,h)=[int(v) for v in bbox]
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2,1)
   else:
        cv2.putText(frame,'Error',(100,0),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
   cv2.imshow('Tracking',frame)
   if cv2.waitKey(1) & 0XFF==27:
        break
cv2.destroyAllWindows()