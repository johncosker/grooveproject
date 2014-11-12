#!/usr/bin/python
import utils
import logging
from song_control import songs_controller
from groove_control import groove_controller

def sqliteManager(data):
    song_controller = songs_controller(1)
    if data['cmd'] == 'addSong':
        song_controller.addKnownSong({'song':   data['song'],
                                      'artist': data['artist'],
                                      'stream': data['stream']})
    elif data['cmd'] == 'addSongAndroid':
        arr = data['info'].split(';')
        song_controller.addKnownSong({'song':   arr[0],
                                      'artist': arr[1],
                                      'stream': arr[2]})
    elif data['cmd'] == 'addSongBySourceType':
        song_controller.addSongBySourceType(data)
    elif data['cmd'] == 'fetchdb':
        pass


class SearchHandler():
    def search(self, string):
        gc = groove_controller(None)
        return gc.getManySongs(string, 20)

    def handle(self, string):
        d = threads.deferToThread(self.search, string)
        d.addCallback(self.ret)
        d.addErrback(self.err)

    def ret(self, data):
        response = {}
        response['type'] = 'json'
        response['songs'] = data
        response['queryType'] = 'search'
        return response

    def err(self, failure):
        self.write('An error occured : %s\n' % failure.getErrorMessage())
        print('An error occured : %s\n' % failure.getErrorMessage())


class main_parser():
    """This takes all networks messages and parses the request commands and
       payload.  This class assumes that all messages have been standarised by
       time they reach this point."""

    def __init__(self, player_q):
        self.response = {}
        self.player_q = player_q
        self._target_parse{'player': self._player,
                           'dataBase': self._dataBase,
                           'search': self._search}
   
    def self.parse_message(self, received_msg):
        self.received_msg = received_msg
        print('dataReceived')
        logging.info(self.received_msg)
        self._target_parse[self.received_msg['target']]()
        return self.response

    def self._player(self):
        self.player_q.put(self.received_msg)
        self.response['type'] = 'Message'
        self.response['Message'] = 'Received'

    def self._dataBase(self):
        if self.received_msg['cmd'] == 'delete':
            song_controller.removeSongById(self.received_msg['info'])
            self.response['type'] = 'Message'
            self.response['Message'] = 'Received'

        elif self.received_msg['cmd'] == 'showdb':
            self.response['type'] = "json"
            self.response['queryType'] = 'database'
            songs = song_controller.toArray()
            self.response['songs'] = songs

        sqliteManager(self.received_msg)
        self.response['type'] = 'Message'
        self.response['Message'] = 'Received'

    def self._search(self):
        h = SearchHandler()
        self.response = h.handle(self.received_msg['cmd'])