import utils
import vlc
from grooveshark import Client
from vlc_control import vlc_controller
from groove_control import groove_controller
gc = groove_controller()
vc = vlc_controller()

def handleInput(string):
	#skip is just for testing for now, should look into better ways to control vlc
	if (string == 'skip'):
		vc.nextSong()
	elif (string == 'print'):
		vc.printList()
	elif (string == 'pause'):
		if(vc.mlp.is_playing):	
			vc.pause()
		else:
			vc.play()
	else:
		vc.addSong(gc.getSong(string))
		if not vc.mlp.is_playing():
			#start plaing the last song in the queue
			vc.mlp.play_item_at_index(vc.mlist.count() - 1)

while True:
	newName = raw_input("Enter song to queue: ")
	handleInput(newName)
