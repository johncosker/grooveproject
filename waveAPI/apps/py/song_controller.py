import sqlite3
import sys

class songs_controller:
	def __init__(self):
		self.con = sqlite3.connect('db/songs.db')
		with self.con:
			self.cur = self.con.cursor()
			self.cur.execute("DROP TABLE IF EXISTS Songs")
                        self.cur.execute("CREATE TABLE Songs(Name TEXT, Artist TEXT, Votes INT,  Url TEXT)")
	def addSong(self, song):
		songTuple = (song.name, song.artist.name, 1, song.stream.url)
		self.cur.execute("INSERT INTO Songs VALUES(?,?,?,?)", songTuple)
		self.con.commit()
