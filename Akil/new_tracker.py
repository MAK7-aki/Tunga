import cv2
import numpy as np
from collections import deque
import datetime


pts = deque(maxlen=40)
center = None
initBB = None
dat = datetime.datetime.now()
prev = None

kf = cv2.KalmanFilter(4,2)
kf.measurementMatrix = np.array([[1, 0, 0, 0],[0, 1, 0, 0]], np.float32)
kftransitionMatrix = np.array([[1, 0, 1, 0],[0, 1, 0, 1],[0, 0, 1, 0],[0, 0, 0, 1]], np.float32)

#vs = VideoStream(src="rtsp://192.168.43.1:8554/fpv_stream").start()
#vs = VideoStream(src=0).start()
frame=cv2.VideoCapture("rtsp://admin:tunga@2020@192.168.168.64")
# frame = cv2.resize(frame, (640, 480))
tracker = cv2.legacy.TrackerMOSSE_create()
bbox = []

while True:
    
    # (H, W) = frame.shape[:2]
    H=480
    W=640
    centroid = (W/2,H/2)
    #cv2.drawMarker(frame, centroid, (0,255,255),0,30,thickness=2)
    if initBB is not None:
        (success, box) = tracker.update(frame)
        if success:
        
            (x, y, w, h) = [int(v) for v in box]
            bb_centroid = ((2*x+w)/2,(2*y+h)/2)
            ey = (2*y+h)/2
            ex = (2*x+w)/2
            prev_x = ex
            prev_y = ey
            if prev_x==0 and prev_y==0:

                erx = prev_x - (W/2)
                ery = prev_y - (H/2)

            erx = prev_x - (W/2)
            ery = prev_y - (H/2)
            kf.correct(np.array((bb_centroid),np.float32))
            retval = kf.predict() 
            prev = retval
            cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 255, 255), 2)
            #cv2.rectangle(frame, (int(x2[0][0]), int(y2[0][0])), (int(x2[0][0]) + w, int(y1[0][0]) + h),(0, 255, 255), 2)
            a = (erx,ery)
            pts.append(bb_centroid)
            # ser.write(str(a))
        elif not success:
            tracker = cv2.legacy.TrackerMOSSE_create()			
            initBB = (prev[0][0]-50,prev[1][0]-50,100,100)
            tracker.init(frame, initBB)
            a = (320,240)
            # ser.write(str(a))	
        for i in range(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue
            
            cv2.line(frame, pts[i - 1], pts[i], (255, 255,255), 2)
    #cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    bbox = frame
    # cf		or tracking, a for photo, b for pilot window (serial read)

    if key == ord("a"):
        cv2.imwrite('Image_Day '+str(dat.strftime("%d/%m/%Y %H:%M:%S"))+'.jpg',frame)

    elif key == ord("c"):

        if initBB is not None:
        
            initBB = None
            # ser.write('e')

        else:
        
            tracker = cv2.legacy.TrackerMOSSE_create()		
            initBB = (W/2 - 100 ,H/2 - 100, 150 ,150)
            tracker.init(frame,  initBB)

    elif key == ord("q"):
        break

cv2.destroyAllWindows()