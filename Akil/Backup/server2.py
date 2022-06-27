import socket
from subprocess import call
import os
import psutil
import time
from pymavlink import mavutil
from _thread import *
import threading

 
#localIP     = "192.168.168.2"

localPort   = 14001

bufferSize  = 1024


UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

util = False
# rs = False

# Bind to address and ip

UDPServerSocket.bind(('',localPort))


print("UDP server up and listening")

def clear_string():

    s = open("/home/tunga/Desktop/Akil/string.txt","w")
    s.truncate(0)
    s.close()

def stream(b):

    r = open("/home/tunga/Desktop/Akil/box.txt","w")
    r.write(b)
    r.close()

# # thread function
def connect():
    while True:

        time.sleep(1)
        # msg3 = b'TA'+b'\x02'+b'\x0f'+b'\x01'+b'\x10'

        c = psutil.cpu_percent(1)#CPU
        r = psutil.virtual_memory().percent#RAM

        c = int(c)
        r = int(r)
        print(c,r)
        bytesToSend1         = c.to_bytes(1,"big")
        bytesToSend2         = r.to_bytes(1,"big")
        ut1 = sum(b'\x0f'+b'\x01'+bytesToSend1+bytesToSend2+b'\x01').to_bytes(1,"big")
        ut2 = sum(b'\x0f'+b'\x01'+bytesToSend1+bytesToSend2+b'\x00').to_bytes(1,"big")
        auto = open("/home/tunga/Desktop/Akil/auto.txt","r+").read()


        if util == True and auto =="0":
            msg1 = b'TA'+b'\x05'+b'\x0f'+b'\x01'+bytesToSend1+bytesToSend2+b'\x01'
        elif util == True and auto =="1":
            msg1 = b'TA'+b'\x05'+b'\x0f'+b'\x01'+bytesToSend1+bytesToSend2+b'\x00'
        elif util == False and auto =="1":
            msg1 = b'TA'+b'\x05'+b'\x0f'+b'\x01'+b'\x00'+b'\x00'+b'\x00'
        else:
            msg1 = b'TA'+b'\x05'+b'\x0f'+b'\x01'+b'\x00'+b'\x00'+b'\x01'

        UDPServerSocket.sendto(msg1,address)
        print("info has sent")
        print(msg1)

while(True):

    master = mavutil.mavlink_connection("/dev/ttyUSB0", baud=115200)
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    data= bytesAddressPair[0]

    address = bytesAddressPair[1]
    print(address)
    string=open("/home/tunga/Desktop/Akil/read.txt","r+")
    d=string.read()
    ls = 1 + len(d)
    # sc = sum(b'\x0e'+str.encode(d)).to_bytes(2,"little")
    msg2 = b'TA'+ls.to_bytes(1,"little")+b'\x0e'+str.encode(d)

    print(data)
    d=""
    k=0
    info = [data[i:i + 1] for i in range(0, len(data))]
    l=len(info)
    valid = int.from_bytes(info[l-1],"little")
    print(valid)
    length = int.from_bytes(info[2],"little")
    # print(length)
    print(info)
    if (info[0] == b'T' and info[1] == b'A'):
        cmd = [data[i:i + 1] for i in range(3,len(data))]
        val = [cmd[i:i + 1] for i in range(0,length)]
        # for i in range(0,length):
        #     k+=int.from_bytes(cmd[i],"little")
        #     print(k)
        # if k == valid:

        #     print("valid command")
        if cmd[0]==b'\x0b' and cmd[1]== b'\x01':
            if(length>2):
                for i in range(2,length):
                    d=d+cmd[i].decode("utf-8")
            s = open("/home/tunga/Desktop/Akil/string.txt","w")
            s.write(d)
            s.close()
            
            # os.system("pkill -f /home/tunga/Desktop/Akil/auto_stream.py")
            # os.system("pkill -f /home/tunga/Desktop/Akil/ot_stream.py")
            stream("1")

        elif cmd[0]==b'\x0b' and cmd[1]== b'\x00':
           
            # os.system("pkill -f /home/tunga/Desktop/Akil/ot_stream.py")
            # os.system("pkill -f /home/tunga/Desktop/Akil/auto_stream.py")
            clear_string()
            stream("0")        
            # call(["gnome-terminal", "--", "sh", "-c", "python3 /home/tunga/Desktop/Akil/auto_stream.py; bash"])
            
        elif cmd[0]==b'\x0c' and cmd[1]== b'\x01':
            
            # os.system("pkill -f /home/tunga/Desktop/Akil/ot_stream.py")
            # os.system("pkill -f /home/tunga/Desktop/Akil/auto_stream.py")
            clear_string()
            stream("2")
            # call(["gnome-terminal", "--", "sh", "-c", "python3 /home/tunga/Desktop/Akil/ot_stream.py; bash"])

        elif cmd[0]==b'\x0c' and cmd[1]== b'\x00':
            
            # os.system("pkill -f /home/tunga/Desktop/Akil/ot_stream.py")
            # os.system("pkill -f /home/tunga/Desktop/Akil/auto_stream.py")
            clear_string()
            stream("0")
            r = open("/home/tunga/Desktop/Akil/auto.txt","w")
            r.write("0")
            r.close()
            master.mav.command_long_send(master.target_system, master.target_component,
                                    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 0, 0, 0, 0, 0, 0, 0)

            msg = master.recv_match(type='COMMAND_ACK', blocking=True)
            print(msg)
        elif cmd[0]==b'\n' and cmd[1]== b'\x01':

            master.mav.command_long_send(master.target_system, master.target_component,
                                    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

            msg = master.recv_match(type='COMMAND_ACK', blocking=True)
            print(msg)

        elif cmd[0]==b'\n' and cmd[1]== b'\x02':

            master.mav.command_long_send(master.target_system, master.target_component,
                                    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 0, 0, 0, 0, 0, 0, 0)

            msg = master.recv_match(type='COMMAND_ACK', blocking=True)
            print(msg)

        elif cmd[0]==b'\r':

            os.system("pkill -f /home/tunga/Desktop/Akil/auto_stream.py")
            call(["gnome-terminal", "--", "sh", "-c", "python3 /home/tunga/Desktop/Akil/auto_stream.py; bash"])

        #     util = True
            # thread = threading.Thread(target = connect)
            # thread.start()
        

        elif cmd[0]==b'\x0f' and cmd[1]== b'\x01':
            
            # if cmd[2] != b'\x01':
            
            #     os.system("pkill -f /home/tunga/Desktop/Akil/auto_stream.py")
            #     call(["gnome-terminal", "--", "sh", "-c", "python3 /home/tunga/Desktop/Akil/auto_stream.py; bash"])
            if cmd[2] == b'\x01':
                util = True
            else:
                thread = threading.Thread(target = connect)
                thread.start() 
                stream("0")
                clear_string()
                r = open("/home/tunga/Desktop/Akil/auto.txt","w")
                r.write("0")
                r.close()

        elif cmd[0]==b'\x0e' and cmd[1]== b'\x01':

            # rs = True
            UDPServerSocket.sendto(msg2, address)
            print(msg2)
            print("read the string")
            
            
        # else:
        #     print("not valid")
        
    else:
        print("error")
    

    # # Sending a reply to client

# UDPServerSocket.close()