import itertools
import utils
import vlc
from grooveshark import Client
from vlc_control import vlc_controller
from groove_control import groove_controller
from song_controller import songs_controller
gc = groove_controller()
vc = vlc_controller()
sc = songs_controller()

def handleInput(string):
	#skip is just for testing for now, should look into better ways to control vlc
	if (string == 'skip'):
		vc.nextSong()
	elif (string == 'print'):
		vc.printList()
	elif (string == 'all'):
		artist = raw_input("Enter name: ")
		songs = itertools.islice(gc.getAll(artist),0,20)
		for song in songs:
			vc.addSong(song)	
		vc.play()
	elif (string == 'pause'):
		vc.pause()
	elif (string == 'play'):
		vc.play()
	else:
		song = gc.getSong(string)
		vc.addSong(song)
		sc.addSong(song)
		if not vc.mlp.is_playing():
			#start plaing the last song in the queue
			vc.mlp.play_item_at_index(vc.mlist.count() - 1)

while True:
	newName = raw_input("Enter song to queue: ")
	handleInput(newName)
