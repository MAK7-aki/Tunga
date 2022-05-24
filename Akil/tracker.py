import cv2

cap =cv2.VideoCapture("rtsp://admin:tunga@2020@10.223.45.100")

tracker = cv2.TrackerMOSSE_create()
success,img = cap.read()


bbox = cv2.selectROI("Tracking",img,False)
tracker.init(img,bbox)
def drawBox(img,bbox):
    pass

while True:
    timer = cv2.getTickCount()
    success,img = cap.read()

    success,bbox = tracker.update(img)
    print(type(bbox))
    if success:
        drawBox(img,bbox)
    else:
        cv2.putText(frame,"lost",(75,75),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

        
    frame = cv2.resize(img,(640,480))

    fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    cv2.putText(frame,str(int(fps)),(75,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
    cv2.imshow("Tracking",frame)


    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break