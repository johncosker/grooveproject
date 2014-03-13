##############################
# Play a song from a passed song name
# 
# Will play the first playable song returned from a search for that song name
##############################

from __future__ import print_function

import subprocess
import argparse

from grooveshark import Client

# param: gen, a generator created by grooveshark Client search(), contains multiple songs
def play(songName):
	client = Client()
	client.init()
	songs = client.search(songName, type='Songs')
	noError = False	# Is set to true if a song plays without error
	while not noError:
		song = songs.next()
		artist = song.artist
		try:
			print('\033[92m' + song.name + " - " + artist.name + " [" + song.duration + "]" + '\033[0m')
#print(song)
			subprocess.call(["cvlc","-q", "-I", "rc", song.stream.url]) 
			noError = True
		except TypeError:
			print("Song Error")
			noError = False
	return
