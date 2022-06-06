import cv2
from pymavlink import mavutil

master = mavutil.mavlink_connection("/dev/ttyUSB0", baud=115200)
master.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %
      (master.target_system, master.target_component))
tracker = cv2.TrackerMOSSE_create()
video = cv2.VideoCapture("rtsp://admin:tunga@2020@192.168.168.64")
bbox = None


while True:
    ok,frame=video.read()
    frame = cv2.resize(frame, (640, 480), \
            interpolation = cv2.INTER_LINEAR)

    if bbox is not None :
        ok,bbox=tracker.update(frame)
        if ok:
            (x,y,w,h)=[int(v) for v in bbox]
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2,1)
        else:
            bbox = None
            cv2.putText(frame,'Error',(100,0),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

    cv2.imshow('Tracking',frame)
    key = cv2.waitKey(1) & 0XFF
        
    if key == ord("a"):
        tracker = cv2.TrackerMOSSE_create()
        bbox = (270 ,190, 100 ,150)
        tracker.init(frame,bbox)
        master.mav.command_long_send(master.target_system, master.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

        msg = master.recv_match(type='COMMAND_ACK', blocking=True)
        print(msg)

    elif key == ord('w'):
        bbox = None
        master.mav.command_long_send(master.target_system, master.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 0, 0, 0, 0, 0, 0, 0)

        msg = master.recv_match(type='COMMAND_ACK', blocking=True)
        print(msg)

    elif key == ord("q"):
        break

cv2.destroyAllWindows()