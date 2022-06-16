import cv2
import sys

tracker = cv2.legacy.TrackerMOSSE_create()
video = cv2.VideoCapture("rtsp://admin:tunga@2020@192.168.168.64")
bbox = None
v=1

while True:
    ok,frame=video.read()
    frame = cv2.resize(frame, (640, 480), \
            interpolation = cv2.INTER_LINEAR)

    if bbox is not None :
        ok,bbox=tracker.update(frame)
        print(bbox)
        if ok:
            (x,y,w,h)=[int(v) for v in bbox]
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2,1)
        else:
            bbox = None
            cv2.putText(frame,'Error',(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

    cv2.imshow('Tracking',frame)
    key = cv2.waitKey(1) & 0XFF
        
    if v==1:
        tracker = cv2.legacy.TrackerMOSSE_create()
        bbox = (270 ,190, 100 ,150)
        tracker.init(frame,bbox)
        v=v+1

    # elif v>1 and bbox == None:
    #     v=1

    elif key == ord("q"):
        break

cv2.destroyAllWindows()