#!/usr/bin/python

import getopt
import sys
import os
import argparse
import subprocess
from shutil import copyfile
from shutil import move

# Path to the configuration-files
dir_path = os.path.dirname(os.path.realpath(__file__)) + "/wifiData"
# Destination-paths for the configurations
path_Hostapd = "/etc/hostapd.conf"
path_Interfaces = "/etc/network/interfaces"
path_Dnsmasq = "/etc/dnsmasq.conf"


def preventive_query(question, default="no"):
    """
    Security query to prevent to overwrite important settings. 
    Default must be negative.
    """
    
    # List of valid answers    
    valid = {"yes":"true",   "y":"true",  "ye":"true",
             "no":"false",     "n":"false"}

    while 1:
        sys.stdout.write(question + "[yes/NO]\n")
        choice = input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no'\n")

def data_setup(filename, destpath):
    """
    Setup of all the necessary files for a simple running wifi.
    Modify the data in the "/wifiData" folder in your project-directory.
    If the files already exists they are stored in a .bak-file
    """
    
    if preventive_query("The file " + destpath + " is going to be modified. OK?")=="true":
        # Check if file already exists
        if os.path.isfile(destpath):
            # If so, store previous version in .bak-file
            copyfile(destpath, destpath + ".bak" )
            print ("Backup copy: " + destpath + ".bak was created.")
        else:
            print (destpath + " created.")
        # Copy the file to the destination path
        copyfile(dir_path + "/" + filename, destpath)
    else: 
        print ("Failed. Process aborted. Backup is getting restored.")
        restore_backup()
        
def restore_backup():
    counter = 0
    if os.path.isfile(path_Hostapd + ".bak"):
        move(path_Hostapd + ".bak", path_Hostapd)
        print ("moved")
        counter += 1
    if os.path.isfile(path_Interfaces + ".bak"):
        move(path_Interfaces + ".bak", path_Interfaces)
        counter += 1
    if os.path.isfile(path_Dnsmasq + ".bak"):
        move(path_Dnsmasq + ".bak", path_Dnsmasq)
        counter += 1
    print ("Sucessfully restored %d files." % counter)
    sys.exit(1)
    
def usage(): 
    print ("This Script is setting up your wifi device as an forwarding AP")
    print ("The standart settings are using eth0 and wlan0 as defaults.")
    print ("If your set up is different consider a modifcation of the %s file" % path_Hostapd)
    print ("Usage:")
    print ("sudo python3 createWifi.py [-r | -s | -h]")
    print ("-r\t\trestore all files with backup-files")
    print ("-s\t\tshut the AP down")
    sys.exit(1)
    
    
try:
    opts, args = getopt.getopt(sys.argv[1:],"hrs",["help"])
except getopt.GetoptError:
      usage()
      sys.exit(1)
for opt, arg in opts:
    if opt == '-r':
        restore_backup()
    elif opt == '-s':
        subprocess.call(['sudo', 'service','hostapd', 'stop'])
        print ("Service stopped!")
        sys.exit(1)
    elif opt in ("-h", "--help"):
        usage()
        

data_setup ("hostapd.conf", path_Hostapd)
data_setup ("interfaces", path_Interfaces)
data_setup ("dnsmasq.conf", path_Dnsmasq)

check = subprocess.call(['sudo', '/etc/init.d/networking', 'restart'])
if check != 0: 
    print ("Please check if the names of your network-devices are set properly in \"wifiData/interfaces\".")
    print ("They might not be \"eth0\" and \"wifi0\" as set in the default values.")
subprocess.call(['sudo', 'hostapd', '-B' , path_Hostapd])


#subprocess.call('ifconfig')
