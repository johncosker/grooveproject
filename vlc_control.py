import utils
import vlc
from grooveshark import Client
class vlc_controller:
	def __init__(self):
		vlc_args = ["-q"]
		self.instance = vlc.libvlc_new(len(vlc_args),vlc_args)
		self.mlist = self.instance.media_list_new()
		self.player = self.instance.media_player_new()
		self.mlp = self.instance.media_list_player_new()
		self.mlp.set_media_player(self.player)
		self.mlp.set_media_list(self.mlist)
		self.em = self.player.event_manager()
		self.em.event_attach(vlc.EventType.MediaPlayerEndReached, self.songFinished)
	def getPlayer(self):
		return self.player
	def getList(self):
		return self.mlist
	def getMLP(self):
		return self.mlp
	def getInstance(self):
		return self.instance
	def addSong(self, song):
		try:
			media = self.instance.media_new(song.stream.url)
			media.set_meta(vlc.Meta.Title, song.name)
			media.set_meta(vlc.Meta.Artist, song.artist.name)
			self.mlist.add_media(media)
			print('\033[92m' + song.name + " - " + song.artist.name + '\033[0m' + " was added to the list")
		except Exception:
			pass
	def play(self):           
		self.mlp.play()
	def pause(self):
		self.mlp.pause()
	def remove(self, index):
		self.mlist.remove_index(index)
	def nextSong(self):
		self.mlp.next()
	def printList(self):
		now = self.player.get_media().get_meta(vlc.Meta.Title)
		for media in self.mlist:
			#media = self.mlist.item_at_index(i)
			if now == media.get_meta(vlc.Meta.Title):
				print('\033[92m' + media.get_meta(vlc.Meta.Title) + " - " + media.get_meta(vlc.Meta.Artist) + '\033[0m' )
			else:
				print (media.get_meta(vlc.Meta.Title) + " - " + media.get_meta(vlc.Meta.Artist))
	def songFinished(self, data):
		pass
