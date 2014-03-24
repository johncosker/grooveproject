#!/usr/bin/env python
#TODO:
"""
Add response from server to return confirmation
"""
import json
import cgi
import socket
import sys

from time import sleep
from multiprocessing.connection import Client
from array import array
from time import sleep

UDP_IP = "192.168.1.16"
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

msgToSend = "{'cmd':%s, 'user':%s, 'target':%s, 'info':%s}" % ( cmd, user, target, info )

sock = socket.socket(socket.AF_INET, # Internet
             socket.SOCK_DGRAM,      # UDP
             socket.IPPROTO_UDP)     # Multicast recvier
             
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
sock.sendto(msgToSend, (UDP_IP, UDP_PORT))


print "Command Sent"
