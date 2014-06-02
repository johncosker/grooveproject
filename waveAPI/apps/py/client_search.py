#!/usr/bin/python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
from grooveshark import Client
import json

print "Content-type: application/json"
print 

client = Client()
client.init()

def parseCmd(msg):
    if len(msg) < 3:
        msg = ""
    else:
        msg = msg[2:-2]
    return msg
'''
cmdRequest = cgi.FieldStorage()

cmd = parseCmd( str(cmdRequest.getlist('cmd')) )
user = parseCmd( str(cmdRequest.getlist('user')) )
target = parseCmd( str(cmdRequest.getlist('target')) )
info = parseCmd( str(cmdRequest.getlist('info')) )
'''
info = 'weezer'
foundSongs = client.search(info, type='Songs')

returnData = []
songCount = 0
for song in foundSongs:
    returnData.append({'song' : song.name, 'artist' : song.artist.name, 'album' : song.album.name, 'stream' : song.stream.url})
    songCount += 1
    if songCount > 19:
        break   

print json.dumps(returnData)