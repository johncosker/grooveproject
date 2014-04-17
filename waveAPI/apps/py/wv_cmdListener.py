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
from groove_control import groove_controller

# Write PID file of the daemon
def writePid():
    pid = str(os.getpid())
    pidfile = "/var/run/wv_interfaceInformer.pid"
    file(pidfile, 'w').write(pid)

# Configures the UDP listener to exept cmds
def listenerStart():
    
    logging.basicConfig(filename='/var/log/python.log',
                        format='Wave Player - %(message)s',
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

def sqliteManager(data):
    cmd = data['cmd']

# Main process loop
def main(listener, player_q, slq_q):
    #search = groove_controller()
    while True:
        cmdMsg = listener.recv(10240)
        logging.info(cmdMsg)
        parsedCmdMsg = literal_eval(cmdMsg)
        # unpack json object
        logging.info(parsedCmdMsg)
        if parsedCmdMsg['target'] == 'player':
            player_q.put(parsedCmdMsg)
        elif parsedCmdMsg['target'] == 'dataBase':
            sqliteManager(parsedCmdMsg)
        #elif parsedCmdMsg['target'] == 'search':
        #    search.getAll(parsedCmdMsg['info'])

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
"""
