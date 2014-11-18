#!/usr/bin/python
import utils
from grooveshark import Client
import vlc


class groove_controller:
    def __init__(self, manager):
        self.client = Client()
        self.client.init()
        self.manager = manager

    def checkSong(self, song):
        instance = vlc.libvlc_new(1, ["-q"])
        try:
            media = instance.media_new(song.stream.url)
            return True
        except TypeError:
            print("Error found adding: " + '\033[92m' + song.name + '\033[0m' + " searching for playable version")
            return False

    def getSong(self, songName):
        songs = self.client.search(songName, type='Songs')
        try:
            song = songs.next()
            while True:
                if self.checkSong(song):
                    print("Found: " + '\033[92m' + song.name + " - " + song.artist.name + '\033[0m')
                    return song
                else:
                    song = songs.next()
        except Exception as e:
            return "Error"
        def getAll(self, songName):
            art = self.client.search(songName, Client.ARTISTS)
            return art.next().songs

    def getManySongs(self, search ,n):
        foundSongs = self.client.search(search)
        returnData = []
        songCount = 0
        while songCount < n:
            song = foundSongs.next()
            returnData.append({'song' : song.name, 'artist' : song.artist.name, 'album' : song.album.name, 'stream' : song.stream.url})
            songCount += 1
        return returnData