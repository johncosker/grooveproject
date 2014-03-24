#!/usr/bin/env python
from __future__ import print_function

import cgi
import cgitb; cgitb.enable
import os
import time


import logging
import subprocess
from grooveshark import Client
from multiprocessing import Process

logging.basicConfig(filename='/var/log/python.log',
                        format='WAVE - %(message)s',
                        level=logging.DEBUG)

client = Client()
client.init()

logging.info('started')

class playerManager(object):
    def __init__(self, queue):
        logging.info("class sarted")

        while True:
            if queue.get:
                recvievedCmd = queue.get()
                logging.info("from worker: %s" % (recvievedCmd))
                if recvievedCmd['cmd'] == 'play':
                    self.play()
                
    def play(self):
        logging.info("starting to play pop list")
        logging.info("Playing PopList")
        for song in client.popular():
            subprocess.call(['mplayer', song.stream.url])