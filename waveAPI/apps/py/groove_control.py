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
        song = songs.next()
        while True:
            if self.checkSong(song):
                print("Found: " + '\033[92m' + song.name + " - " + song.artist.name + '\033[0m')
                return song
            else:
                song = songs.next()
    def getAll(self, songName):
        art = self.client.search(songName, Client.ARTISTS)
        return art.next().songs

