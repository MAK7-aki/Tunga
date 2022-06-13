from subprocess import call

k="on"
call(["gnome-terminal", "--", "sh", "-c", "python3 /home/tunga/Desktop/Akil/ot_stream.py %s; bash"%k])
# sudo pkill -9 python
# from server import c

# print(c)