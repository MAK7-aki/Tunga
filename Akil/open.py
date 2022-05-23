import cv2
from imutils.video import VideoStream

cv2.namedWindow("RTSP View", cv2.WINDOW_NORMAL)
cap = cv2.VideoCapture("rtsp://127.0.0.1:8554/video_stream")
while True:
    
    ret, frame = cap.read()
    if ret:
        cv2.imshow("RTSP View", frame)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('e'): # e key ends process
            break
    else:
        print("unable to open camera")
        break
cap.release()
cv2.destroyAllWindows()