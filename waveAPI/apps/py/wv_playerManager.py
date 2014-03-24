#!/usr/bin/env python
from __future__ import print_function

import cgi
import cgitb; cgitb.enable
import os
import time
import itertools
import utils
import vlc
import logging
import subprocess

from grooveshark import Client
from multiprocessing import Process
from grooveshark import Client
from vlc_control import vlc_controller
from groove_control import groove_controller
from song_controller import songs_controller

class playerManager(object):
    def __init__(self, queue):
        logging.basicConfig(filename='/var/log/python.log',
                        format='WAVE - %(message)s',
                        level=logging.DEBUG)
        self.client = Client()
        self.client.init()
        self.gc = groove_controller()
        self.vc = vlc_controller()
        self.sc = songs_controller()

        logging.info('started')

        logging.info("playerManager sarted")

        # Get next command
        while True:
            if queue.get:
                self.recvievedCmd = queue.get()
                logging.info("from worker: %s" % (self.recvievedCmd))
                self.handelInput(self.recvievedCmd['cmd'])
                
    def playPopular(self):
        logging.info("starting to play pop list")
        logging.info("Playing PopList")
        for song in self.client.popular():
            self.vc.addSong(song)
            self.vc.play()

    def handleInput(self, string):
        #skip is just for testing for now, should look into better ways to control vlc
        if (string == 'skip'):
            self.vc.nextSong()
        elif (string == 'print'):
            self.vc.printList()
        elif (string == 'all'):
            self.artist = raw_input("Enter name: ")
            self.songs = itertools.islice(self.gc.getAll(artist),0,20)
            for song in songs:
                self.vc.addSong(song)
            self.vc.play()
        elif (string == 'pause'):
            self.vc.pause()
        elif (string == 'play'):
            self.vc.play()
        elif (string == 'popular'):
            self.playPopular()
        else:
            self.song = self.gc.getSong(sself.tring)
            self.vc.addSong(self.song)
            self.sc.addSong(self.song)
            if not self.vc.mlp.is_playing():
                #start plaing the last song in the queue
                self.vc.mlp.play_item_at_index(self.vc.mlist.count() - 1)