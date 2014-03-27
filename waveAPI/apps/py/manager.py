import itertools
import utils
import vlc
from grooveshark import Client
from vlc_control import vlc_controller
from groove_control import groove_controller
from song_control import songs_controller

class manager:
	#Create controllers
	def __init__(self):
		self.gc = groove_controller(self)
		self.vc = vlc_controller(self)
		self.sc = songs_controller(self)
		
        #Play the list, good for initially starting player
	def play(self):
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
		if (string == 'skip'):
			self.skip()
		elif (string == 'print'):
			self.printList()
		elif (string == 'pause'):
			self.pauseToggle()
		elif (string == 'play'):
			self.play()
		elif (string == 'gethighest'):
			print self.sc.getHighest()
		else:
			self.add(string)
	def run(self):
		while True:
			newName = raw_input("Enter song to queue: ")
			self.handleInput(newName)

m = manager()
m.run()
