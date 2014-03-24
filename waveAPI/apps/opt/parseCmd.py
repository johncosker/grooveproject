#!/usr/bin/python
#TODO:
"""
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
"""
import json
import cgi

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


"""
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