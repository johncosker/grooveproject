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

TCP_IP = utils.get_ip_address('eth0')
TCP_PORT = 5055
BUFFER_SIZE = 1024

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

socketInst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketInst.connect((TCP_IP, TCP_PORT))
socketInst.send(msgToSend)
data = socketInst.recv(BUFFER_SIZE)
socketInst.close()

print data
