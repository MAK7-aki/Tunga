from imutils.video import VideoStream

import imutils
import cv2
import serial

vs= VideoStream(src="rtsp://admin:tunga@2020@10.223.45.100").start()

while True:
    frame =  vs.read()
    if frame is None:
        break
    frame = imutils.resize(frame, height=480,width=640)

    
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('e'): # e key ends process
        break

vs.stop()
cv2.destroyAllWindows()