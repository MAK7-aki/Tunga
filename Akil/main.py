from subprocess import call
import os

data =b'TA\x02\x0e\x01'
k=0
d=""
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
    print(val)
    for i in range(0,length):
        k+=int.from_bytes(cmd[i],"little")
    print(k)

        
    # if k==valid:
    #     print("valid command")
    if cmd[0]==b'\x0e' and cmd[1]== b'\x01':
        string=open("read.txt","r+")
        d=string.read()
    print(d)
    # if cmd[0]==b'\x0b' and cmd[1]== b'\x01':
    #     if(length>2):
    #         for i in range(2,length):
    #             d=d+cmd[i].decode("utf-8") 
    #         string=open("string.txt","w")
    #         string.truncate(0)
    #         string.write(d)
    #         string.close()
    #     os.system("pkill -f /home/grimm/Desktop/Akil/camera.py")
    #     call(["gnome-terminal", "--", "sh", "-c", "python3 /home/grimm/Desktop/Akil/detect.py; bash"])
    # elif cmd[0]==b'\x0b' and cmd[1]== b'\x00':
    #     os.system("pkill -f /home/grimm/Desktop/Akil/detect.py")
    #     call(["gnome-terminal", "--", "sh", "-c", "python3 /home/grimm/Desktop/Akil/camera.py; bash"])
    # else:
    #     print("not valid")

    
else:
    print("error")


