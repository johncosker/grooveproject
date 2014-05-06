#!/usr/bin/env python
from __future__ import print_function

import cgi
import cgitb; cgitb.enable
import os
import time
import itertools
import vlc
import logging
import subprocess

from multiprocessing import Process
from grooveshark import Client
from vlc_control import vlc_controller
from groove_control import groove_controller
from song_control import songs_controller

class playerManager(object):
    def __init__(self, queue):
        logging.basicConfig(filename='/var/log/python.log',
                format='WAVE - %(message)s',
                level=logging.DEBUG)
        self.client = Client()
        self.client.init()
        self.gc = groove_controller(self)
        self.vc = vlc_controller(self)
        self.sc = songs_controller(self)

        logging.info('started')

        logging.info("playerManager sarted")

        # Get next command
        while True:
            if queue.get:
                recievedCmd = queue.get()
                logging.info("from worker: %s" % (recievedCmd))
                self.handleInput(recievedCmd['cmd'])

    def playPopular(self):
        logging.info("starting to play pop list")
        logging.info("Playing PopList")
        for song in self.client.popular():
            self.vc.addSong(song)
        self.vc.play()
        
    def play(self):
        logging.info("Player: play()")
        self.vc.play()

    def pauseToggle(self):
        if self.vc.isPlaying():
            self.vc.pause()
        else:
            self.vc.play()

    def skip(self):
        self.addNextSong()
        self.vc.nextSong()

    #Pring the vlc playlist, will not include songs in db
    def printList(self):
        self.vc.printList()

    #Add a song to the database
    def add(self, string):
        song = self.gc.getSong(string)
        self.sc.addSong(song)
        if self.vc.count() == 0:
            self.addNextSong()

    #Pull next song from DB and add to vlc_controller
    def addNextSong(self):
        row = self.sc.getHighest()
        self.vc.addSongRow(row)	

    def handleInput(self, string):
        print("Input: " + string)
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
