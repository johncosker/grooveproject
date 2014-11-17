#!/usr/bin/python
import utils
import logging
from song_control import songs_controller
from groove_control import groove_controller


class main_parser():
    """This takes all networks messages and parses the request commands and
       payload.  This class assumes that all messages have been standarised by
       time they reach this point."""

    def __init__(self, player_q):
        self.response = {}
        self.player_q = player_q

    def _player(self):
        def player_player(self):
                self.player_q.put(self.received_msg)
                self.response['type'] = 'Message'
                self.response['Message'] = 'Received'

        player_options = {'player' : player_player}
        cmd = self.received_msg['cmd']
        player_options[cmd](self)

    def _dataBase(self):
        def db_delete(self):
            self.song_controller.removeSongById(self.received_msg['info'])
            self.response['type'] = 'Message'
            self.response['Message'] = 'Received'

        def db_showdb(self):
            self.response['type'] = "json"
            self.response['queryType'] = 'database'
            songs = self.song_controller.toArray()
            self.response['songs'] = songs

        def db_addSong(self):
            self.song_controller.addKnownSong({'song': data['song'],
                                               'artist': data['artist'],
                                               'stream': data['stream']})
            self.response['type'] = 'Message'
            self.response['Message'] = 'Received'

        def db_addSongAndriod(self):
            self.song_controller.addKnownSong({'song': arr[0],
                                               'artist': arr[1],
                                               'stream': arr[2]})
            self.response['type'] = 'Message'
            self.response['Message'] = 'Received'

        def db_addSongBySourceType(self):
            self.song_controller.addSongBySourceType(data)
            self.response['type'] = 'Message'
            self.response['Message'] = 'Received'

        def db_fetchdb(self):
            self.response['type'] = 'Message'
            self.response['Message'] = 'Received'

        self.song_controller = songs_controller(1)
        dataBase_options = {'delete': db_delete,
                            'showdb': db_showdb,
                            'addSong': db_addSong,
                            'addSongAndroid': db_addSongAndriod,
                            'addSongBySourceType': db_addSongBySourceType,
                            'fetchdb': db_fetchdb}
        target = self.received_msg['target']
        dataBase_options[target](self)

    def _search(self):
        def search_search(self):
                gc = groove_controller(None)
                self.response['type'] = 'json'
                self.response['songs'] = gc.getManySongs(string, 20)
                self.response['queryType'] = 'search'

        search_options = {'search': search_search}
        target = self.received_msg['target']
        search_options[target](self)

    def parse_message(self, received_msg):
        """Main parser function"""
        target_parse = {'player': self._player,
                        'dataBase': self._dataBase,
                        'search':  self._search}
        self.received_msg = received_msg
        print('dataReceived')
        logging.info(self.received_msg)
        target = self.received_msg['target']
        target_parse[target]()
        return self.response