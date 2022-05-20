from imutils.video import VideoStream
from collections import deque

import imutils
import cv2
import datetime

pts = deque(maxlen=20)
initBB = None
tracker = cv2.TrackerMOSSE_create()

vs = VideoStream(src="rtsp://admin:tunga@2020@10.223.45.100").start()


while True:

	frame =  vs.read()

	if frame is None:
		break
	
	frame = imutils.resize(frame, height=480,width=640)
	(H, W) = frame.shape[:2]
	centroid = (W/2,H/2)

	if  initBB is not None:
		(success, box) = tracker.update(frame)
		if success:
		
			(x, y, w, h) = [int(v) for v in box]
			bb_centroid = ((2*x+w)/2,(2*y+h)/2)
			ey = (2*y+h)/2 - H/2
			ex = (2*x+w)/2 - W/2

			cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 255, 255), 2)

			a = (round(ex),round(ey),2000)

			pts.append(bb_centroid)


		elif not success:
			initBB = None
			a = (320,240)	

		for i in range(1, len( pts)):
			if  pts[i - 1] is None or  pts[i] is None:
				continue
	
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("a"):
		tracker = cv2.TrackerMOSSE_create()
		initBB = (W/2 - 50 ,H/2 - 50, 100 ,150)
		tracker.init(frame,  initBB)

	elif key == ord('w'):
		initBB = None
		
	elif key == ord("q"):
	 	break

vs.stop()
cv2.destroyAllWindows()
