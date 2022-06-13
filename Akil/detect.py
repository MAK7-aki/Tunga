import cv2
import numpy as np
# from pymavlink import mavutil

cap = cv2.VideoCapture("rtsp://admin:tunga@2020@192.168.168.64")
# master = mavutil.mavlink_connection("/dev/ttyUSB0", baud=115200)
# master.wait_heartbeat()
# print("Heartbeat from system (system %u component %u)" %
#       (master.target_system, master.target_component))

ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    frame1 = cv2.resize(frame1, (640, 480))
    frame2 = cv2.resize(frame2, (640, 480))
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # master.mav.command_long_send(master.target_system, master.target_component,
    #                                 mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 0, 0, 0, 0, 0, 0, 0)

    # msg = master.recv_match(type='COMMAND_ACK', blocking=True)
    # print(msg)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 900:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)
        # master.mav.command_long_send(master.target_system, master.target_component,
        #                              mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

        # msg = master.recv_match(type='COMMAND_ACK', blocking=True)
        # print(msg)
        
        

    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
cap.release()
