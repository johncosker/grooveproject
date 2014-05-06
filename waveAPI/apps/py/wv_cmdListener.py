#!/usr/bin/python
# UDP multicast listener
import json
import socket
import struct
import logging
import os
import json
import wv_playerManager
import time
import utils

from multiprocessing import Queue
from multiprocessing import Process
from ast import literal_eval
from groove_control import groove_controller
from song_control import songs_controller
import SocketServer

TCP_IP = utils.get_ip_address('eth0')
TCP_PORT = 5055
BUFFER_SIZE = 1024

song_controller = songs_controller(1)

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        response = {}
        self.data = self.request.recv(1024).strip()
        parsedCmdMsg = json.loads(self.data)
        logging.info(parsedCmdMsg)
        if parsedCmdMsg['target'] == 'player':
            player_q.put(parsedCmdMsg)
            response['type'] = "Message"
            response['Message'] = "Received"
        elif parsedCmdMsg['target'] == 'dataBase':
            sqliteManager(parsedCmdMsg)
            response['type'] = "Message"
            response['Message'] = "Received"
        elif parsedCmdMsg['target'] == 'searcher':
            # response = song_controller.toJSON()
            response['type'] = "json"
            songs = song_controller.toArray()
            response['songs'] = songs
        self.request.send(json.dumps(response))
        self.request.send("\n")

# Write PID file of the daemon
def writePid():
    pid = str(os.getpid())
    pidfile = "/var/run/wv_interfaceInformer.pid"
    file(pidfile, 'w').write(pid)

# Starts the player instance that recieves commands from Queue (player_q)
def startPlayerWorker(q):
    #playerInstance = wv_playerManager.playerManager(q)
    worker = Process(target=wv_playerManager.playerManager, args = (q,))
    worker.daemon = True
    worker.start()

# Starts SQLite instance that recieves commands from Queue (slq_q)
def startSqlWorker(q):
    tmp = 1

def sqliteManager(data):
    if data['cmd'] == 'addSong':
        song_controller.addKnownSong({'song' : data['song'],
                                      'artist' : data['artist'],
                                      'stream' : data['stream']})
    elif data['cmd'] == 'fetchdb':
        tmp = 1

# Main process loop
def main(player_q, slq_q):
    try:
        server = SocketServer.TCPServer((TCP_IP, TCP_PORT), MyTCPHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print "Exiting"
        server.shutdown()

# __init__
if __name__ == "__main__":
    logging.basicConfig(filename='/var/log/python.log',
                        format='Wave Player - %(message)s',
                        level=logging.DEBUG)
    writePid()
    player_q = Queue()
    slq_q = Queue()
    startPlayerWorker(player_q)
    startSqlWorker(slq_q)
    main(player_q, slq_q)

"""
#TODO:
-Replace all prints
    -Change them all to a foo that will create a json 
        object to return
    -Object should include errors, success
    
-Connect to running media player to submitt command
   -each command should call its own foo in the media
        player
       -these commands can also be used for internal
            media player use

-add handling for adding songs to the db
    -this should be the song ID, client it is loaded from
        -only allow songs from verified clients (at first)
    
-add handling for up/down boat
    -these commnds should include the unique SQL id
    
-add get all entries in db
    -prepair these to json
    -maybe include a quick update that only includes changed
        data in the db
        -votes/order
        -have the agent use this info to rearange the dataTable    
"""
