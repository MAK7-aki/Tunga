import socket
from subprocess import call
import os
import psutil
from pymavlink import mavutil
from _thread import *
import threading

 
#localIP     = "192.168.168.2"

localPort   = 14001

bufferSize  = 1024


UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


ram=False
# Bind to address and ip

UDPServerSocket.bind(('',localPort))


print("UDP server up and listening")

# # thread function
def ram():
    while True:
        c=psutil.cpu_percent(1)#CPU
        r=psutil.virtual_memory().percent#RAM

        c=int(c)
        r=int(r)
        print(c,r)
        bytesToSend1         = c.to_bytes(1,"big")
        bytesToSend2         = r.to_bytes(1,"big")
        msg1 = b'TA'+b'\x03'+b'\x0d'+bytesToSend1+bytesToSend2
        # print(msg1)

        # data received from client
        # data = t.recv(1024)           
            # lock released on exit
            # print_lock.release()
            # break

        # reverse the given string from client
        # data = data[::-1]

        # send back reversed string to client
        UDPServerSocket.sendto(msg1,address)
        print("info has sent")
        print(msg1)
        
    
    # connection closed
    # t.close()

# Listen for incoming datagrams
# thread = threading.Thread(target=ram)

while(True):

    master = mavutil.mavlink_connection("/dev/ttyUSB0", baud=115200)
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    data= bytesAddressPair[0]

    address = bytesAddressPair[1]
    print(address)

    string=open("/home/tunga/Desktop/Akil/read.txt","r+")
    d=string.read()
    msg2 = b'TA'+b'\x0b'+b'\x0e'+str.encode(d)

    # data = "Message from Client:{}".format(clientMsg)
    # clientIP  = "Client IP Address:{}".format(address)
    print(data)
    d=""
    k=0
    info = [data[i:i + 1] for i in range(0, len(data))]
    l=len(info)
    valid = int.from_bytes(info[l-1],"little")
    # print(valid)
    length = int.from_bytes(info[2],"little")
    # print(length)
    print(info)
    if (info[0] == b'T' and info[1] == b'A'):
        cmd = [data[i:i + 1] for i in range(3,len(data))]
        val = [cmd[i:i + 1] for i in range(0,length)]

        if cmd[0]==b'\x0b' and cmd[1]== b'\x01':
            if(length>2):
                for i in range(2,length):
                    d=d+cmd[i].decode("utf-8")

            os.system("pkill -f /home/tunga/Desktop/Akil/b_stream.py")
            os.system("pkill -f /home/tunga/Desktop/Akil/dl_stream.py")
            os.system("pkill -f /home/tunga/Desktop/Akil/ot_stream.py")
            os.system("pkill -f /home/tunga/Desktop/Akil/st_stream.py")
            call(["gnome-terminal", "--", "sh", "-c", "python3 /home/tunga/Desktop/Akil/b_stream.py %s; bash"%d])

        elif cmd[0]==b'\x0b' and cmd[1]== b'\x00':
            os.system("pkill -f /home/tunga/Desktop/Akil/b_stream.py")
            os.system("pkill -f /home/tunga/Desktop/Akil/ot_stream.py")
            os.system("pkill -f /home/tunga/Desktop/Akil/dl_stream.py")
            os.system("pkill -f /home/tunga/Desktop/Akil/st_stream.py")
            call(["gnome-terminal", "--", "sh", "-c", "python3 /home/tunga/Desktop/Akil/dl_stream.py; bash"])
            
        elif cmd[0]==b'\x0c' and cmd[1]== b'\x01':
            os.system("pkill -f /home/tunga/Desktop/Akil/b_stream.py")
            os.system("pkill -f /home/tunga/Desktop/Akil/ot_stream.py")
            os.system("pkill -f /home/tunga/Desktop/Akil/dl_stream.py")
            os.system("pkill -f /home/tunga/Desktop/Akil/st_stream.py")
            call(["gnome-terminal", "--", "sh", "-c", "python3 /home/tunga/Desktop/Akil/ot_stream.py; bash"])

        elif cmd[0]==b'\x0c' and cmd[1]== b'\x00':
            os.system("pkill -f /home/tunga/Desktop/Akil/b_stream.py")
            os.system("pkill -f /home/tunga/Desktop/Akil/ot_stream.py")
            os.system("pkill -f /home/tunga/Desktop/Akil/dl_stream.py")
            os.system("pkill -f /home/tunga/Desktop/Akil/st_stream.py")
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

        elif cmd[0]==b'\r' and cmd[1]== b'\x01':

            thread = threading.Thread(target=ram)
            thread.start()

        
        elif cmd[0]==b'\x0e' and cmd[1]== b'\x01':
            
            UDPServerSocket.sendto(msg2, address)
            print("read the string")
            
        # else:
        #     print("not valid")
        
    else:
        print("error")
    

    # # Sending a reply to client

# UDPServerSocket.close()