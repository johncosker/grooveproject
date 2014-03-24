#!/usr/bin/python

from __future__ import print_function
from grooveshark import Client

import logging
import os
import subprocess

print ("Content-Type: text/html")     # HTML is following
print ("")                            # blank line, end of headers

#logging.basicConfig(filename='/var/log/message', filemode='w', level=logging.DEBUG)
#logging.info("starting to play pop list")
client = Client()
client.init()
print ("running")

#logging.info("Playing PopList")
for song in client.popular():
    subprocess.call(['mpg123', song.stream.url])
    
