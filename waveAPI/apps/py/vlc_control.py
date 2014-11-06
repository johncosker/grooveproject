#!/usr/bin/python
import utils
utils.setSystemSettings()
import vlc
from grooveshark import Client


class vlc_controller:

    def __init__(self, manager):
        vlc_args = [""]
        self.instance = vlc.libvlc_new(len(vlc_args),vlc_args)
        self.mlist = self.instance.media_list_new()
        self.player = self.instance.media_player_new()
        self.mlp = self.instance.media_list_player_new()
        self.mlp.set_media_player(self.player)
        self.mlp.set_media_list(self.mlist)
        self.em = self.player.event_manager()
        self.em.event_attach(vlc.EventType.MediaPlayerEndReached, self.songFinished)
        self.manager = manager

    # Old addSong method using song objects, currently unused
    def addSong(self, song):
        try:
            media = self.instance.media_new(song.stream.url)
            media.set_meta(vlc.Meta.Title, song.name)
            media.set_meta(vlc.Meta.Artist, song.artist.name)
            self.mlist.add_media(media)
            print('\033[92m' + song.name + " - " + song.artist.name + '\033[0m' + " was added to the list")
        #This is a pretty bad way of handling exceptions
        except Exception:
            pass

    # Adds a song to the media list from a sqlite row object
    def addSongRow(self, row):
        media = self.instance.media_new(row['Url'])
        media.set_meta(vlc.Meta.Title, row['Name'])
        media.set_meta(vlc.Meta.Artist, row['Artist'])
        print('\033[92m' + media.get_meta(vlc.Meta.Title) + " - " + media.get_meta(vlc.Meta.Artist) + '\033[0m' )
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

    # Callback function called when a song ends, notifies the manager that a song ended and a new song should be added to the playlist
    def songFinished(self, data):
        self.manager.addNextSong()
