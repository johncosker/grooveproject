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
        msg = msg[2:-2]
    return msg

cmdRequest = cgi.FieldStorage()

cmd = parseCmd( str(cmdRequest.getlist('cmd')) )
user = parseCmd( str(cmdRequest.getlist('user')) )
target = parseCmd( str(cmdRequest.getlist('target')) )
info = parseCmd( str(cmdRequest.getlist('info')) )

msgToSend = {'cmd' : cmd, 'user' : user, 'target' : target, 'info' : info}

if cmd == 'addSong': 
    song = parseCmd( str(cmdRequest.getlist('song')) )
    album = parseCmd( str(cmdRequest.getlist('album')) )
    artist = parseCmd( str(cmdRequest.getlist('artist')) )
    stream = parseCmd( str(cmdRequest.getlist('stream')) )

    msgToSend['song'] = song
    msgToSend['album'] = album
    msgToSend['artist'] = artist
    msgToSend['stream'] = stream

send_data = json.dumps(msgToSend)

socketInst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketInst.connect((TCP_IP, TCP_PORT))
socketInst.send(send_data)
socketInst.send("\n")
data = socketInst.recv(BUFFER_SIZE)
socketInst.close()

print data
