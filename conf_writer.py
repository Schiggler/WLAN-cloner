import sys
import os

#Path to hostapd.conf file
conf_path = "/home/schick/workspace/WLAN-cloner/startWifi/wifiData/hostapd.conf"


#Check if an argument was given
if len(sys.argv) < 2:
    file_name = os.path.basename(sys.argv[0])
    print "Usage: python {} <WLAN interface>".format(file_name)
    sys.exit(0)
    
#The first parameter is the given interface
new_interface = sys.argv[1]
    
#Open the conf file and extract its text as a list of lines
f = open(conf_path,'r')
filedata = f.readlines()
f.close()


#Replace the first line with the new ssid
filedata[1] = "interface={}\n".format(new_interface)


#Concatinate the list to a single string (needed for writing into a new file)
new_conf_text = ""
for i in filedata:
    new_conf_text += i


#Open the hostapd.conf file again and overwrite everything with the new configuration text
f = open(conf_path,'w')
f.write(new_conf_text)
f.close()

print "hostapd.conf edited. Added {} as a new interface".format(new_interface)
