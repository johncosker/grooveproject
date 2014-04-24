import sqlite3
import sys

class songs_controller:
    # Initialize controller, maybe need to explore thread safety
    def __init__(self, manager):
        self.con = sqlite3.connect('/opt/grooveproject/waveAPI/db/songs.db', check_same_thread=False)
        self.con.text_factory = str
        self.con.row_factory = sqlite3.Row
        with self.con:
            self.cur = self.con.cursor()
            self.cur.execute("DROP TABLE IF EXISTS Songs")
            self.cur.execute("CREATE TABLE Songs(Name TEXT, Artist TEXT, Votes INT,  Url TEXT)")

    # Add a song to the db, right now votes is only separate for testing, in the future all initial votes will be 0
    def addSong(self, song):
        if not self.checkExists(song.name):
            songTuple = (song.name, song.artist.name, 1, song.stream.url)
            self.cur.execute("INSERT INTO Songs VALUES(?,?,?,?)", songTuple)
        else:
            self.cur.execute("UPDATE Songs SET Votes = Votes + 1 WHERE Name = ?", (song.name,))
        self.con.commit()

    # Add a song with a know stream URL
    def addKnownSong(self, song):
        if not self.checkExists(song['song']):
            songTuple = (song['song'], song['artist'], 1, song['stream'])
            self.cur.execute("INSERT INTO Songs VALUES(?,?,?,?)", songTuple)
        else:
            self.cur.execute("UPDATE Songs SET Votes = Votes + 1 WHERE Name = ?", (song['song'],))
        self.con.commit()

    # Gets the row with the highest vote count, if the highest is -1, reset all songs to 0 
    def getHighest(self):
        self.cur.execute("SELECT rowid, * FROM Songs WHERE Votes = (SELECT MAX(Votes) FROM Songs) LIMIT 1")
        row = self.cur.fetchone()
        if row['Votes'] == -1:
            self.resetList()
        self.cur.execute("UPDATE Songs SET Votes = -1 WHERE rowid = ?", (row['rowid'],))
        self.con.commit()
        return row

    # Resets all songs to 0 in case there are no new songs, this cauess the played songs to be playable again
    def resetList(self):
        self.cur.execute("UPDATE Songs SET Votes = 0")

    # Check for duplicate song name
    def checkExists(self, song):
        self.cur.execute("SELECT 1 FROM Songs WHERE Name = ?", (song,))
        if self.cur.fetchone():
            return 1
        else:
            return 0


