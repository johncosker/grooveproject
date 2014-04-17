#!/usr/bin/env python
import json
import cgi
import socket
import sys
import logging
import utils

from time import sleep
from multiprocessing.connection import Client
from array import array
from time import sleep

UDP_IP = utils.get_ip_address('eth0')
UDP_PORT = 4242

print ("Content-Type: text/html")     # HTML is following
print ("")                            # blank line, end of headers

def parseCmd(msg):
    if len(msg) < 3:
        msg = "''"
    else:
        msg = msg[1:-1]
    return msg

cmdRequest = cgi.FieldStorage()

cmd = parseCmd( str(cmdRequest.getlist('cmd')) )
user = parseCmd( str(cmdRequest.getlist('user')) )
target = parseCmd( str(cmdRequest.getlist('target')) )
info = parseCmd( str(cmdRequest.getlist('info')) )
#info += parseCmd( str(cmdRequest.getlist('info')) )
#info = cmdRequest.getlist('info')

msgToSend = "{'cmd':%s, 'user':%s, 'target':%s, 'info':%s}" % ( cmd, user, target, info )

sock = socket.socket(socket.AF_INET, # Internet
             socket.SOCK_DGRAM,      # UDP
             socket.IPPROTO_UDP)     # Multicast recvier
             
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
sock.sendto(msgToSend, (UDP_IP, UDP_PORT))


print "Command Sent"
