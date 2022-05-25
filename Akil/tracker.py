import cv2

tracker = cv2.TrackerMOSSE_create()
video = cv2.VideoCapture("rtsp://admin:tunga@2020@10.223.45.100")
# ok,img=video.read()

# frame = cv2.resize(img,(640,480))
bbox = None

# ok = tracker.init(frame,bbox)

while True:
    ok,frame=video.read()
    # try:
    frame = cv2.resize(frame, (640, 480), \
            interpolation = cv2.INTER_LINEAR)
    # except Exception as e:
    #     pass
    # if not ok:
    #     break
    if bbox is not None :
        ok,bbox=tracker.update(frame)
        if ok:
            (x,y,w,h)=[int(v) for v in bbox]
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2,1)
        else:
            bbox = None
            cv2.putText(frame,'Error',(100,0),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

    cv2.imshow('Tracking',frame)
    key = cv2.waitKey(1) & 0XFF
        
    if key == ord("a"):
        tracker = cv2.TrackerMOSSE_create()
        bbox = (270 ,190, 100 ,150)
        tracker.init(frame,bbox)

    elif key == ord('w'):
        bbox = None

    elif key == ord("q"):
        break

cv2.destroyAllWindows()