# t = sum(b'\x0f'+b'\x01').to_bytes(1,"big")
# # a=t.to_bytes(1,"big")
# print(t)
# import base64

# string=open("/home/tunga/Desktop/Akil/read.txt","r+")
# d=string.read()
# # msg2 = b'TA'+b'\x0b'+b'\x0e'+ base64.b64encode(d)
# print(base64.b64encode(str.encode(d)))
# r= sum(b'\x0e'+ base64.b64encode(d))
# k=r.to_bytes(2,"big")
# print(r)
# print(k)
# print(msg2)
# for i in range(0,5):
#     print("helo")
auto = open("/home/tunga/Desktop/Akil/auto.txt","r+").read()

print(auto)