#!/usr/bin/python
import utils
import vlc
import logging
from time import sleep
from multiprocessing import Queue, Process
from grooveshark import Client
from vlc_control import vlc_controller
from groove_control import groove_controller
from song_control import songs_controller

def start_playerManager():
    """Starts the player instance that recieves commands from Queue (player_q)"""
    player_q = Queue()
    worker = Process(target = playerManager, args = (player_q,))
    worker.daemon = True
    worker.start()
    return player_q


class playerManager(object):
    def __init__(self, queue):
        self.client = Client()
        self.client.init()
        self.gc = groove_controller(self)
        self.vc = vlc_controller(self)
        self.sc = songs_controller(self)

        logging.info('playerManager sarted')

        # Get next command
        while True:
            if queue.get:
                recievedCmd = queue.get()
                logging.info('raw cmd: %s' % (recievedCmd))
                self.handleInput(recievedCmd['cmd'])

    def wait():
        sleep(15)

    def playPopular(self):
        logging.info('starting to play pop list')
        logging.info('Playing PopList')
        for song in self.client.popular():
            self.vc.addSong(song)
        self.vc.play()

    def play(self):
        logging.info('Player: play()')
        self.vc.play()

    def pauseToggle(self):
        if self.vc.isPlaying():
            self.vc.pause()
        else:
            self.vc.play()

    def skip(self):
        self.addNextSong()
        self.vc.nextSong()

    # Pring the vlc playlist, will not include songs in db
    def printList(self):
        self.vc.printList()

    # Add a song to the database
    def add(self, string):
        logging.info('STRING : ' + string)
        song = self.gc.getSong(string)
        if not song == 'Error':
            self.sc.addSong(song)
            if self.vc.count() == 0:
                self.addNextSong()
        else:
            print ( "Error getting song" )

    # Pull next song from DB and add to vlc_controller
    def addNextSong(self):
        row = self.sc.getHighest()
        self.vc.addSongRow(row)

    def handleInput(self, string):
        print('Input: ' + string)
        if (string == 'skip'):
            self.skip()
        elif (string == 'print'):
            self.printList()
        elif (string == 'pause'):
            self.pauseToggle()
        elif (string == 'play'):
            self.play()
        else:
            self.add(string)