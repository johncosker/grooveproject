#!/usr/bin/python
import utils
import logging
from song_control import songs_controller
from groove_control import groove_controller
from wv_playerManager import playerManager


class main_parser():
    """This takes all networks messages and parses the request commands and
       payload.  This class assumes that all messages have been standarised by
       time they reach this point."""

    def __init__(self):
        logging.info("Made Parser")
        self.response = {'type': 'Message',
                         'Message': 'Received'}
        self.player = playerManager()

    def _player(self):
        def player_play(self):
            self.player.play()
        def player_pause(self):
            self.player.pause()
        def player_skip(self):
            self.player.skip()
        def player_current(self):
            self.response['type'] = 'json'
            self.response['song'] = self.player.currentSong()
            self.response['queryType'] = 'search'

        player_options = {'play': player_play,
                            'skip': player_skip,
                            'pause': player_pause,
                            'current': player_current}
        cmd = self.received_msg['cmd']
        player_options[cmd](self)

    def _dataBase(self):
        def db_delete(self):
            self.song_controller.removeSongById(self.received_msg['info'])

        def db_showdb(self):
            self.response['type'] = "json"
            self.response['queryType'] = 'database'
            songs = self.song_controller.toArray()
            self.response['songs'] = songs

        def db_addSong(self):
            self.song_controller.addKnownSong({'song': self.received_msg['song'],
                                               'artist': self.received_msg['artist'],
                                               'stream': self.received_msg['stream']})

        def db_addSongAndriod(self):
            self.song_controller.addKnownSong({'song': arr[0],
                                               'artist': arr[1],
                                               'stream': arr[2]})

        def db_addSongBySourceType(self):
            self.song_controller.addSongBySourceType(self.received_msg)

        def db_fetchdb(self):
            pass

        self.song_controller = songs_controller()
        dataBase_options = {'delete': db_delete,
                            'showdb': db_showdb,
                            'addSong': db_addSong,
                            'addSongAndroid': db_addSongAndriod,
                            'addSongBySourceType': db_addSongBySourceType,
                            'fetchdb': db_fetchdb}
        cmd = self.received_msg['cmd']
        dataBase_options[cmd](self)

    def _search(self):
        def search_search(self):
                gc = groove_controller(None)
                self.response['type'] = 'json'
                self.response['songs'] = gc.getManySongs(self.received_msg['info'],
                                                         20)
                self.response['queryType'] = 'search'

        search_options = {'search': search_search}
        cmd = self.received_msg['cmd']
        search_options[cmd](self)

    def parse_message(self, received_msg):
        """Main parser function"""
        target_parse = {'player': self._player,
                        'dataBase': self._dataBase,
                        'search':  self._search}
        self.received_msg = received_msg
        logging.info(self.received_msg)

        if self.received_msg['target'] in target_parse.keys():
            target = self.received_msg['target']
            target_parse[target]()
        else:
            print("FUCK THIS SHIT %s" % self.received_msg['target'])
        return self.response
