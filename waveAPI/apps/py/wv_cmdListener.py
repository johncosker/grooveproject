#!/usr/bin/python
# UDP multicast listener
import socket
import struct
import logging
import os
import json
import wv_playerManager
import time

from multiprocessing import Queue
from multiprocessing import Process
from ast import literal_eval

# Write PID file of the daemon
def writePid():
    pid = str(os.getpid())
    pidfile = "/var/run/wv_interfaceInformer.pid"
    file(pidfile, 'w').write(pid)

# Configures the UDP listener to exept cmds
def listenerStart():
    
    logging.basicConfig(filename='/var/log/python.log',
                        format='CMD - %(message)s',
                        level=logging.DEBUG)

    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM,
                         socket.IPPROTO_UDP)
                         
    sock.setsockopt(socket.SOL_SOCKET,
                    socket.SO_REUSEADDR,
                    1)
                    
    sock.bind(('', 4242))
    # wrong: mreq = struct.pack("sl", socket.inet_aton("224.51.105.104"), socket.INADDR_ANY)
    mreq = struct.pack("=4sl",
                       socket.inet_aton("224.51.105.104"),
                       socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return sock

# Starts the player instance that recieves commands from Queue (player_q)
def startPlayerWorker(q):
    #playerInstance = wv_playerManager.playerManager(q)
    worker = Process(target=wv_playerManager.playerManager, args = (q,))
    worker.daemon = True
    worker.start()

# Starts SQLite instance that recieves commands from Queue (slq_q)
def startSqlWorker(q):
    tmp = 1
    """
    worker = Process(target=wavePlayer, args = (q,))
    worker.daemon = True
    worker.start()
    """

#call correct functions on running player thread
def play():
    print "play"
    #conn.send('close')

def pause():
    print "pause"
    #conn.send('close')
    
def skip():
    print "skip"
    #conn.send('close')

def upSong():
    print "upSong"
    #conn.send('close')

def downSong():
    print "downSong"
    #conn.send('close')
    
# Main process loop
def main(listener, player_q, slq_q):

    while True:
        cmdMsg = listener.recv(10240)
        logging.info(cmdMsg)
        parsedCmdMsg = literal_eval(cmdMsg)
        # unpack json object
        logging.info(parsedCmdMsg)
        if parsedCmdMsg['target'] == 'player':
            player_q.put(parsedCmdMsg)

# __init__
if __name__ == "__main__":
    writePid()
    listener = listenerStart()
    player_q = Queue()
    slq_q = Queue()
    startPlayerWorker(player_q)
    startSqlWorker(slq_q)
    main(listener, player_q, slq_q)


"""
#TODO:
-Replace all prints
    -Change them all to a foo that will create a json object to return
    -Object should include errors, success
    
-Connect to running media player to submitt command
   -each command should call its own foo in the media player
       -these commands can also be used for internal media player use

-add handling for adding songs to the db
    -this should be the song ID, client it is loaded from
        -only allow songs from verified clients (at first)
    
-add handling for up/down boat
    -these commnds should include the unique SQL id
    
-add get all entries in db
    -prepair these to json
    -maybe include a quick update that only includes changed data in the db
        -votes/order
        -have the agent use this info to rearange the dataTable

import json
import cgi
import socket
import struct

from time import sleep
from multiprocessing.connection import Client
from array import array

print ("Content-Type: text/html")     # HTML is following
print ("")                            # blank line, end of headers

def connMediaPlayer():
    # Ping server / On fail spawn a server process
    # conn.send('close')
    # can also send arbitrary objects:
    # conn.send(['a', 2.5, None, int, sum])
    # conn.close()
    address = ('localhost', 31415)
    try:
        conn = Client(address, authkey='wavePi')
        conn.send('alive')
        while True:
            msg = conn.recv()
            # do something with msg
            if msg == True:
                break

    except:
        tmp = 1
        #conn timed outs
        #process not running, create one and try again
        #subprocess call to start player
        #sleep(2) # allow time for player to start
        #connMediaPlayer() or but all in a for x in range(0,5) loop to allow for max conn attempts

def runCmd(msg):
    cmd = msg.getvalue("cmd", False)
    user = msg.getvalue("user", False)
    info = msg.getvalue("info", False)
    
    # Check for blank fields
    if cmd and user:
    
        # ADMIN COMMANDS
        if user == 'admin':
            if cmd == 'play':
                play()
        
            elif cmd == 'pause':
                pause()
        
            elif cmd == 'skip':
                skip()
        # OTHER CMDS
        if cmd == 'upSong':
            upSong()
        
        elif cmd == 'downSong':
            downSong()
    else:
        print "Wrong command input"

#call correct functions on running player thread
def play():
    print "play"
    #conn.send('close')

def pause():
    print "pause"
    #conn.send('close')
    
def skip():
    print "skip"
    #conn.send('close')

def upSong():
    print "upSong"
    #conn.send('close')

def downSong():
    print "downSong"
    #conn.send('close')


runCmd(cgi.FieldStorage())



    def manual_getAvailableDevice( request ):
    returnData = { "cams": [] }
    if request.method == 'POST':
        nvrconfigDb = libinputconfig_py.CVeApiNVRConfigDatabase(True)
        securityGroup = int( request.POST.get('securityGroup') )
        findList =  simplejson.loads( request.POST.get('list') )
        ipList = libutils_py.StringVec()
        for item in findList:
            ipList.append(str(item))

        req = nvrconfigDb.getManualDiscoveredDeviceList( ipList, securityGroup )
        for device in req:
            mac_addr = ':'.join([device.m_sMacAddress[i:i+2] for i in range(0, len(device.m_sMacAddress), 2)])
            returnData['cams'].append( discCam )

    json = simplejson.dumps ( returnData )
    return HttpResponse( json, mimetype="application/json" )
    
"""