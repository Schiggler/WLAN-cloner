'''
Created on Feb 21, 2017

@author: schick
'''

#Path to hostapd.conf file
conf_path = "/home/schick/workspace/WLAN-cloner/startWifi/wifiData/hostapd.conf"
new_ssid  = "Test_ssid"

#Open the conf file and extract its text as a list of lines
f = open(conf_path,'r')
filedata = f.readlines()
f.close()


#Replace the first line with the new ssid
filedata[1] = "interface={}\n".format(new_ssid)


#Concatinate the list to a single string (needed for writing into a new file)
new_conf_text = ""
for i in filedata:
    new_conf_text += i


#Open the hostapd.conf file again and overwrite everything with the new configuration text
f = open(conf_path,'w')
f.write(new_conf_text)
f.close()

print "hostapd.conf edited. Added {} as a new SSID".format(new_ssid)