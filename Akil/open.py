import cv2

cap = cv2.VideoCapture("rtsp://192.168.168.2:8554/video_stream")
while True:
    ret, frame = cap.read()
 
    if ret:
        cv2.imshow("RTSP View", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
    else:
        print("unable to open camera")
        break
    
cap.release()
cv2.destroyAllWindows()