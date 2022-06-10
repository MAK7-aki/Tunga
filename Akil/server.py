import socket
from subprocess import call
import os
import psutil

 
#localIP     = "192.168.168.2"

localPort   = 14001

bufferSize  = 1024

# c ="hello client"

# bytesToSend1         = str.encode(c)
 

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 

# Bind to address and ip

UDPServerSocket.bind(('',localPort))

 

print("UDP server up and listening")

c=psutil.cpu_percent(2)#CPU
r=psutil.virtual_memory()[2]#RAM

c=int(c)
r=int(r)
bytesToSend1         = c.to_bytes(2,"big")
bytesToSend2         = r.to_bytes(2,"big")

# Listen for incoming datagrams

while(True):


    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    data= bytesAddressPair[0]

    address = bytesAddressPair[1]
    print(address)

    UDPServerSocket.sendto(bytesToSend1, address)
    UDPServerSocket.sendto(bytesToSend2, address)

    # data = "Message from Client:{}".format(clientMsg)
    # clientIP  = "Client IP Address:{}".format(address)
    print(data)
    d=""
    k=0
    info = [data[i:i + 1] for i in range(0, len(data))]
    l=len(info)
    valid = int.from_bytes(info[l-1],"little")
    print(valid)
    length = int.from_bytes(info[2],"little")
    print(length)
    print(info)
    if (info[0] == b'T' and info[1] == b'A'):
        cmd = [data[i:i + 1] for i in range(3,len(data))]
        val = [cmd[i:i + 1] for i in range(0,length)]
        # for i in range(0,length):
        #     k+=int.from_bytes(cmd[i],"little")
        # if k==valid:
            # print("valid command")
        if cmd[0]==b'\x0b' and cmd[1]== b'\x01':
            if(length>2):
                for i in range(2,length):
                    d=d+cmd[i].decode("utf-8") 
                string=open("string.txt","w")
                string.truncate(0)
                string.write(d)
                string.close()
            os.system("pkill -f /home/grimm/Desktop/Akil/dl_stream.py")
            os.system("pkill -f /home/grimm/Desktop/Akil/od_stream.py")
            call(["gnome-terminal", "--", "sh", "-c", "python3 /home/grimm/Desktop/Akil/od_stream.py; bash"])
        elif cmd[0]==b'\x0b' and cmd[1]== b'\x00':
            os.system("pkill -f /home/grimm/Desktop/Akil/od_stream.py")
            os.system("pkill -f /home/grimm/Desktop/Akil/dl_stream.py")
            call(["gnome-terminal", "--", "sh", "-c", "python3 /home/grimm/Desktop/Akil/dl_stream.py; bash"])
        # else:
        #     print("not valid")
        
    else:
        print("error")
    

    # # Sending a reply to client
