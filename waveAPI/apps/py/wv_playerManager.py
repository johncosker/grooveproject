#/usr/bin/python
import utils
import logging
import vlc
from time import sleep
from multiprocessing import Queue, Process
from grooveshark import Client
from groove_control import groove_controller
from song_control import songs_controller

class playerManager(object):
    def __init__(self):
        self.client = Client()
        self.client.init()
        self.sc = songs_controller()
        self.sc.clearSongsTable()

        vlc_args = [""]
        self.instance = vlc.libvlc_new(len(vlc_args),vlc_args)
        self.mlist = self.instance.media_list_new()
        self.player = self.instance.media_player_new()
        self.mlp = self.instance.media_list_player_new()
        self.mlp.set_media_player(self.player)
        self.mlp.set_media_list(self.mlist)
        self.em = self.player.event_manager()
        self.em.event_attach(vlc.EventType.MediaPlayerEndReached, self.songEnded)

    def pauseToggle(self):
        if self.isPlaying():
            self.pause()
        else:
            self.play()

    def skip(self):
        self.addNextSong()
        self.nextSong()

    # Pull next song from DB and add to vlc_controller
    def addNextSong(self):
        row = self.sc.getHighest()
        self.addSongRow(row)

    # Adds a song to the media list from a sqlite row object
    def addSongRow(self, row):
        media = self.instance.media_new(row['Url'])
        media.set_meta(vlc.Meta.Title, row['Name'])
        media.set_meta(vlc.Meta.Artist, row['Artist'])
        print('\033[92m' + media.get_meta(vlc.Meta.Title) + " - " + \
                media.get_meta(vlc.Meta.Artist) + '\033[0m' )
        self.mlist.add_media(media)

    def count(self):
        return self.mlist.count()

    def isPlaying(self):
        return self.mlp.is_playing()

    def play(self):
        self.mlp.play()

    def pause(self):
        self.mlp.pause()

    def remove(self, index):
        self.mlist.remove_index(index)

    def songEnded(self, data):
        self.addNextSong()
        # self.nextSong()

    def nextSong(self):
        self.mlp.next()

    def currentSong(self):
        song = {}
        logging.info( "DERP")
        media = self.player.get_media()
        if media:
            song['name'] = media.get_meta(vlc.Meta.Title)
            song['artist'] = media.get_meta(vlc.Meta.Artist)
            song['album'] = media.get_meta(vlc.Meta.Album)
            song['image'] = media.get_meta(vlc.Meta.ArtworkURL)
        else:
            song['name'] = "no"
            song['artist'] = "fucking"
            song['album'] = "media"
            song['image'] = ""
        logging.info(song)
        return song
