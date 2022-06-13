bbox= (270 ,190, 100 ,150)
file=open('box.txt','w')
for i in bbox:
    file.write(str([i]))
file.close

data=open('box.txt','r+')
box=data.read()

print(box)
data.truncate(0)
data.close

