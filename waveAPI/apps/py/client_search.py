#!/usr/bin/python

import __init__
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
from grooveshark import Client
import json

print "Content-type: application/json"
print ""

client = Client()
client.init()

def parseCmd(msg):
    if len(msg) < 3:
        msg = ""
    else:
        msg = msg[2:-2]
    return msg

cmdRequest = cgi.FieldStorage()

cmd = parseCmd( str(cmdRequest.getlist('cmd')) )
user = parseCmd( str(cmdRequest.getlist('user')) )
target = parseCmd( str(cmdRequest.getlist('target')) )
info = parseCmd( str(cmdRequest.getlist('info')) )

foundSongs = client.search(info, type='Fast')

returnData = []
songCount = 0
for song in foundSongs:
    returnData.append({'song' : song['SongName'],
                       'artist' : song['ArtistName'],
                       'album' : song['AlbumName'],
                       'SongID' : song['SongID'],
                       'ArtistID': song['ArtistID']})
    songCount += 1
    if songCount > 19:
        break

print json.dumps(returnData)
