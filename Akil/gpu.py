import os
import psutil

status = os.system('systemctl is-active --quiet service-name')

try:
      while True:
        print(status)
        print('The CPU usage is: ', psutil.cpu_percent(2))
        print('RAM memory % used:', psutil.virtual_memory()[2])


except KeyboardInterrupt:
    pass
