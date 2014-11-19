#!/usr/bin/python

import json
import cgi
import socket
import logging


TCP_IP = "192.168.1.11"
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

msgToSend = {'cmd': cmd, 'user': user, 'target': target, 'info': info}

if 'addSong' in cmd:
    song = parseCmd( str(cmdRequest.getlist('song')) )
    album = parseCmd( str(cmdRequest.getlist('album')) )
    artist = parseCmd( str(cmdRequest.getlist('artist')) )
    SongID = parseCmd( str(cmdRequest.getlist('SongID')) )
    ArtistID = parseCmd( str(cmdRequest.getlist('ArtistID')) )

    msgToSend['song'] = song
    msgToSend['album'] = album
    msgToSend['artist'] = artist
    msgToSend['SongID'] = SongID
    msgToSend['ArtistID'] = ArtistID

send_data = json.dumps(msgToSend)

socketInst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketInst.connect((TCP_IP, TCP_PORT))
socketInst.send(send_data)
socketInst.send("\n")
data = socketInst.recv(BUFFER_SIZE)
socketInst.close()

print data
