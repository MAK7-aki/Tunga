# import os
import psutil

# status = os.system('systemctl is-active --quiet service-name')


while True:
  c=psutil.cpu_percent(1)#CPU
  r=psutil.virtual_memory().percent#RAM
  c=int(c)
  r=int(r)
  print(c,r)



