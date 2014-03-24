##############################
# Play a song from a passed song name
# 
# Will play the first playable song returned from a search for that song name
##############################

from __future__ import print_function

import subprocess
import argparse
import vlc
from grooveshark import Client

# param: gen, a generator created by grooveshark Client search(), contains multiple songs
def play(songName, player):
	client = Client()
	client.init()
	songs = client.search(songName, type='Songs')
	noError = False	# Is set to true if a song plays without error
	while not noError:
		song = songs.next()
		artist = song.artist
		try:
			print('\033[92m' + song.name + " - " + artist.name +  '\033[0m')
#print(song)
			player.set_mrl(song.stream.url)
			player.play()
			noError = True
		except TypeError:
			print("Song Error")
			noError = False
	return
def printList(mlist):
	i = 0
	for m in mlist:
		print(mlist.item_at_index(i).get_meta(vlc.Meta.Title))
		i=i+1
