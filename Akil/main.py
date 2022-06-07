
data = b'TA\x02\x0b\x01\x00\x0c'
k=0
info = [data[i:i + 1] for i in range(0, len(data))]
l=len(info)
valid = int.from_bytes(info[l-1],"big")
print(valid)
length = int.from_bytes(info[2],"big")
print(length)
print(info)
if (info[0] == b'T' and info[1] == b'A'):
    cmd = [data[i:i + 1] for i in range(3,len(data))]
    val = [cmd[i:i + 1] for i in range(0,length)]
    for i in range(0,length):
        k+=int.from_bytes(cmd[i],"little")
    if k==valid:
        print("valid command")
    else:
        print("not valid")  

else:
    print("error")
# exec(open("/home/grimm/Desktop/Akil/camera.py").read())

