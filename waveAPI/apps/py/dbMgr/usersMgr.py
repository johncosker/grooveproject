#!/usr/bin/python
import utils
import sqlite3
import base64
import uuid
import time

debug = False

class userMgr:
    """Handles / auths all users"""
    def __init__(self, user):
        self.username, self.password, self.uid = base64.decodestring(user).split(':')
        self.con = sqlite3.connect(utils.dbDir + 'users.db',
                                   check_same_thread=False)
        self.con.text_factory = str
        self.con.row_factory = sqlite3.Row
        with self.con:
            self.cur = self.con.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, pass TEXT, uid TEXT)")

    def checkUser(self):
        """Auth User"""
        print 'checkUser'
        print self.username
        print self.password
        print self.uid
        if debug:
            return True
        else:
            if self.uid == 'NULL':
                return self.createUser()
            else:
                self.cur.execute("SELECT * FROM users WHERE uid = (?)", (self.uid,))
                row = self.cur.fetchone()
                if row == None:
                    return False
                if self.username == row[0] and self.password == row[1]:
                    return True
                else:
                    return False

    def createUser(self):
        """Create a new user"""
        uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, self.username + str(time.time() )))
        print uid
        self.cur.execute("INSERT INTO users VALUES(?,?,?)", (self.username, self.password, uid))
        self.con.commit()
        return True


# please ignore v

from grooveshark import Client


class songs_controller:
    def __init__(self):
        self.con = sqlite3.connect(utils.dbDir + 'songs.db',
                                   check_same_thread=False)
        self.con.text_factory = str
        self.con.row_factory = sqlite3.Row
        with self.con:
            self.cur = self.con.cursor()

    def clearSongsTable(self):

            self.cur.execute("DROP TABLE IF EXISTS Songs")
            self.cur.execute("""CREATE TABLE Songs(Name TEXT, Artist TEXT,
                                                 Votes INT,  Url TEXT)""")

    def addSong(self, song, artist, url):
        """Add a song to the db, right now votes is only separate for testing,
            in the future all initial votes will be 0"""
        if not self.checkExists(song):
            songTuple = (song, artist, 1, url)
            self.cur.execute("INSERT INTO Songs VALUES(?,?,?,?)", songTuple)
        else:
            self.cur.execute("UPDATE Songs SET Votes = Votes + 1 WHERE Name = ?",
                             (song,))
        self.con.commit()

    def removeSongById(self, rowid):
        """docstring for removeSongById"""
        self.cur.execute("DELETE FROM Songs WHERE rowid=?", (rowid,))
        self.con.commit()

    def addKnownSong(self, song):
        """Add a song with a know stream URL"""
        if not self.checkExists(song['song']):
            songTuple = (song['song'], song['artist'], 1, song['stream'])
            self.cur.execute("INSERT INTO Songs VALUES(?,?,?,?)", songTuple)
        else:
            self.cur.execute("UPDATE Songs SET Votes = Votes + 1 WHERE Name = ?",
                             (song['song'],))
        self.con.commit()
        print '\033[92m{} - {}\033[0m'.format(song['song'], song['artist'])

    def addSongBySourceType(self, rawData):
        """Add song that does not yet have a stream url"""
        client = Client()
        client.init()
        streamUrl = client.getStreamID(rawData['SongID'], rawData['ArtistID'])
        self.addSong(rawData['song'], rawData['artist'], streamUrl)

    def toArray(self):
        """Dumps Songs table"""
        self.cur.execute("SELECT rowid, Name, Artist, Votes FROM Songs")
        rows = self.cur.fetchall()
        songs = []
        for row in rows:
            songs.append({'name': row['Name'],
                          'artist': row['Artist'],
                          'rowid': row['rowid'],
                          'votes': row['Votes']
                        })
        return songs

    def getHighest(self):
        """Gets the row with the highest vote count, if the highest is -1,
           reset all songs to 0"""
        self.cur.execute("""SELECT rowid, * FROM Songs WHERE Votes =
                            (SELECT MAX(Votes) FROM Songs) LIMIT 1""")
        row = self.cur.fetchone()
        if row['Votes'] == -1:
            self.resetList()
        self.cur.execute("UPDATE Songs SET Votes = -1 WHERE rowid = ?",
                        (row['rowid'],))
        self.con.commit()
        return row

    def resetList(self):
        """Resets all songs to 0 in case there are no new songs, this cauess
           the played songs to be playable again"""
        self.cur.execute("UPDATE Songs SET Votes = 0")

    def checkExists(self, song):
        """Check for duplicate song name"""
        self.cur.execute("SELECT 1 FROM Songs WHERE Name = ?", (song,))
        if self.cur.fetchone():
            return 1
        else:
            return 0