from imutils.video import VideoStream
import imutils
import cv2

vs= VideoStream(src="rtsp://admin:tunga@2020@192.168.168.64").start()
# from subprocess import call

while True:
    frame =  vs.read()
    if frame is None:
        break
    frame = imutils.resize(frame, height=480,width=640)
     
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'): # q key ends process
        break
    # call (["python3","gpu.py"]) 

vs.stop()
cv2.destroyAllWindows()