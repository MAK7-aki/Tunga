import netifaces as ni
ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
print(ip)
print("rtsp://ip:8554/video_stream",ip)
import socket   
hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname)   
print("Your Computer Name is:"+hostname)   
print("Your Computer IP Address is:"+IPAddr)  