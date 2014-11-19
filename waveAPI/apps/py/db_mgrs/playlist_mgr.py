#!/usr/bin/python
import utils
import sqlite3

# TODO :: FINISH : This class is under construction, do not use.
# NOTE wrap all names in []
class playlistMgr:
    """A wrapper class to access the playlist database"""
    def __init__(self):
        self.con = sqlite3.connect(utils.getDBdir()['playlist'], check_same_thread=False)
        self.con.text_factory = str
        self.con.row_factory = sqlite3.Row
        with self.con:
            self.cur = self.con.cursor()

    def setPlaylist(self, playlist):
        """Saves/creates a playlist"""
        self.cur.execute("DROP TABLE IF EXISTS ?", (playlist['name'],))
        self.cur.execute("CREATE TABLE ?(Name TEXT, Artist TEXT, Url TEXT)", (playlist['name'],))
        
        mediaData = playList['entries']
        for media in mediaData:
            self.cur.execute("INSERT INTO ? VALUES(?,?,?)", (playlist['name'], media),)
      
        self.con.commit()

    def getPlayList(self):
        """Gets a playlist by name"""
        pass
        
    def getAllPlayLists(self):
        """Gets list of all playlist names"""
        pass

    def removeplayList(self):
        """docstring for removeSongById"""
        pass