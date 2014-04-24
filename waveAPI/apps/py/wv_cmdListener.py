#!/usr/bin/python
# UDP multicast listener
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

TCP_IP = utils.get_ip_address('eth0')
TCP_PORT = 5055
BUFFER_SIZE = 1024

song_controller = songs_controller(1)


# Write PID file of the daemon
def writePid():
    pid = str(os.getpid())
    pidfile = "/var/run/wv_interfaceInformer.pid"
    file(pidfile, 'w').write(pid)

# Configures the UDP listener to exept cmds
def listenerStart():
    utils.check_for_open_port(TCP_PORT)
    socketInst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketInst.bind((TCP_IP, TCP_PORT))
    socketInst.listen(5)
    return socketInst

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
def main(listener, player_q, slq_q):

    while True:
        conn, addr = listener.accept()
        while True:
            cmdMsg = conn.recv(BUFFER_SIZE)
            if not cmdMsg:
                break
            logging.info(cmdMsg)
            parsedCmdMsg = json.loads(cmdMsg)
            # unpack json object
            logging.info(parsedCmdMsg)
            if parsedCmdMsg['target'] == 'player':
                player_q.put(parsedCmdMsg)
            elif parsedCmdMsg['target'] == 'dataBase':
                sqliteManager(parsedCmdMsg)
            #elif parsedCmdMsg['target'] == 'search':
            #    search.getAll(parsedCmdMsg['info'])

            conn.send("COMPLETE") # echo tcp

# __init__
if __name__ == "__main__":
    logging.basicConfig(filename='/var/log/python.log',
                        format='Wave Player - %(message)s',
                        level=logging.DEBUG)
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
