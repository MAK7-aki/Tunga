from imutils.video import VideoStream
import imutils
import cv2

vs= VideoStream(src="127.0.0.1:8554/stream1 ! application/x-rtp, media=video ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink")
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