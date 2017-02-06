#!/usr/bin/python

from datetime import datetime
from scapy.all import *

iface = "wlan1"

def packet_handler(pkt):
   if pkt.haslayer(Dot11ProbeReq):
      if len(pkt.info) > 0:
         print "{}\tMAC: {}\tSSID:{}".format(datetime.now(), pkt[Dot11].addr2, pkt.info)

print "Sniffing started on {}\n".format(iface)

sniff(iface=iface, prn=packet_handler)
