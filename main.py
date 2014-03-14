import utils
import vlc
import time
from grooveshark import Client
client = Client()
client.init()
songs = client.search("Wake me up", type='Songs')
song = songs.next()
vlc_args = ["-q"]
instance = vlc.libvlc_new(1,vlc_args)

player = instance.media_player_new()
player.set_mrl(song.stream.url)
player.play()
time.sleep(500)
