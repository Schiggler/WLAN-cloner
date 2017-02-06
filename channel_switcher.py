import os, sys, time

"""This script automatically switches between all channels on a given wireless interface"""

wait_time       = 5
switch_command  = "sudo iwconfig {} channel "
interface       = "wlan1"
channels        = (1,2,3,4,5,6,7,8,9,10,11)

while True:

   for channel in channels:
      try:
         os.system(switch_command.format(interface) + str(channel))
      except:
         print "Channel switching failed"
      time.sleep(wait_time)
