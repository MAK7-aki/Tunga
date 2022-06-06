from imutils.video import VideoStream
from collections import deque
import imutils
import cv2
import numpy as np
import keyboard 


pts = deque(maxlen=20)
initBB = None
tracker = cv2.TrackerMOSSE_create()

vs = cv2.VideoCapture("rtsp://admin:tunga@2020@192.168.168.64")

while True:

	frame =  vs.read()

	# if frame is None:
	# 	break
	# #height, width, layers = frame.shape
	# height = 480
	# width = 640
	# H = height / 2
	# W = width / 2
	# resize1 = cv2.resize(frame, (H, W))
	# resize=np.array(resize1)
	# #resize = cv2.resize(frame, (640, 480)) 
	resize = cv2.resize(frame, (640, 480), \
            interpolation = cv2.INTER_LINEAR)
	(H, W) = (640,480)
	centroid = (W/2,H/2)

	if  initBB is not None:
		(success, box) = tracker.update(resize)
		if success:
		
			(x, y, w, h) = [int(v) for v in box]
			bb_centroid = ((2*x+w)/2,(2*y+h)/2)
			ey = (2*y+h)/2 - H/2
			ex = (2*x+w)/2 - W/2

			cv2.rectangle(resize, (x, y), (x + w, y + h),(0, 255, 255), 2)

			#a = (round(ex),round(ey),2000)

			pts.append(bb_centroid)


		elif not success:
			initBB = None
			#a = (320,240)	

		#for i in range(1, len( pts)):
			# if  pts[i - 1] is None or  pts[i] is None:
			# 	continue
	# resize2=np.uint8(resize)
	cv2.imshow("Frame", resize)
	key = cv2.waitKey(1) & 0xFF

	if keyboard.is_pressed('a'):
		tracker = cv2.TrackerMOSSE_create()
		initBB = (W/2 - 50 ,H/2 - 50, 100 ,150)
		tracker.init(resize,  initBB)

	elif keyboard.is_pressed('w'):
		initBB = None
		
	elif keyboard.is_pressed('q'):
	 	break

vs.stop()
cv2.destroyAllWindows()
