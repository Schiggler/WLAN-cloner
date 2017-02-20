#!/usr/bin/python

import getopt
import os
from datetime import datetime
from scapy.all import *

# Wifi-Interface
iface = "wlan0"
# Path to current dir
dir_path = os.path.dirname(os.path.realpath(__file__))
# Initialize logfile
logfile = dir_path + "/sniff.log"
event_counter = 0



def packet_handler(pkt):
    global workfile, event_counter
#    if pkt.haslayer(Dot11ProbeReq):
    #if len(pkt.info) > 0:
    if hasattr(pkt.payload, "src"):
        output_string = '({}) {}\tMAC: {}\tSSID:{}'.format(event_counter, datetime.now(), pkt[Dot11].addr2, pkt.info)
        print output_string
        # Opens or creates the logfile in appending mode
        workfile = open(logfile, 'a')
        workfile.write(output_string+"\n")
        workfile.close
        
        event_counter += 1

def cli_parameter():
    global iface, logfile
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:f:",["help"])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:

        if opt in ("-i"):
            iface = arg
        elif opt in ("-f"):
            logfile = arg
        elif opt in ("-h", "--help"):
            usage()
      
def usage(): 
    
    print"You are sniffing on {}".format(iface)
    print"Outputfile is {}".format(logfile)
    print"Usage:"
    print"sudo python sniff.py -i interface -f file"
    print"-i\t\tName of the Wifi-Interace"
    print"-f\t\tfilename of the \"interfaces\" file"
    sys.exit(1)
    

cli_parameter()

print"Sniffing started on {}".format(iface)
print"Outputfile is {}".format(logfile)


sniff(iface=iface, prn=packet_handler)
