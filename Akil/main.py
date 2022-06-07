
data = b'TA\x02\x0b\x01\x00\x0c'
 
info = [data[i:i + 1] for i in range(0, len(data))]

print(info)
if (info[0] == b'T' and info[1] == b'A'):
    if ( info[2] == b'\x02'):
        for i in info:
            print()
    print("succ")
else:
    print("error")
# exec(open("/home/grimm/Desktop/Akil/camera.py").read())

