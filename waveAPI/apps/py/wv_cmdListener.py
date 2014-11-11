#!/usr/bin/python
import utils
import json
import logging
import wv_playerManager
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet import reactor, threads
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from multiprocessing import Queue
from multiprocessing import Process
from groove_control import groove_controller
from song_control import songs_controller

song_controller = songs_controller(1)
gc = groove_controller(None)

def startPlayerWorker(q):
    """Starts the player instance that recieves commands from Queue (player_q)"""
    worker = Process(target=wv_playerManager.playerManager, args = (q,))
    worker.daemon = True
    worker.start()

def sqliteManager(data):
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

class SearchHandler(object):
    def __init__(self, write_callback):
        self.write = write_callback

    def search(self, string):
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
        self.write(json.dumps(response) + '\n')

    def err(self, failure):
        self.write('An error occured : %s\n' % failure.getErrorMessage())
        print('An error occured : %s\n' % failure.getErrorMessage())

class CmdProtocol(Protocol):

    def connectionMade(self):
        pass

    def dataReceived(self, data):
        print('dataReceived')
        response = {}
        parsedCmdMsg = json.loads(data)
        logging.info(parsedCmdMsg)
        if parsedCmdMsg['target'] == 'player':
            player_q.put(parsedCmdMsg)
            response['type'] = 'Message'
            response['Message'] = 'Received'
            self.transport.write(json.dumps(response))
            self.transport.write("\n")
        elif parsedCmdMsg['target'] == 'dataBase':
            sqliteManager(parsedCmdMsg)
            response['type'] = 'Message'
            response['Message'] = 'Received'
            self.transport.write(json.dumps(response))
            self.transport.write("\n")
        elif parsedCmdMsg['target'] == 'db':
            if parsedCmdMsg['cmd'] == "delete":
                song_controller.removeSongById(parsedCmdMsg['info'])
                response['type'] = "Message"
                response['Message'] = "Received"
                self.transport.write(json.dumps(response))
                self.transport.write("\n")
            elif parsedCmdMsg['cmd'] == "showdb":
                response['type'] = "json"
                response['queryType'] = "database"
                songs = song_controller.toArray()
                response['songs'] = songs
                self.transport.write(json.dumps(response))
                self.transport.write("\n")
        elif parsedCmdMsg['target'] == 'search':
            h = SearchHandler(self.transport.write)
            h.handle(parsedCmdMsg['cmd'])

    def write(self, string):
        self.transport.write(string)

    def err(self, string):
        self.transport.write('Error thing')


class MyFactory(ServerFactory):
    protocol = CmdProtocol

    def __init__(self, player_q):
        self.player_q = player_q


class MyServerProtocol(WebSocketServerProtocol):
    def onMessage(self, payload, isBinary):
        print(':D')
        self.sendMessage(payload, isBinary)

# __init__
if __name__ == '__main__':
    try:
        player_q = Queue()
        startPlayerWorker(player_q)
        factory = MyFactory(player_q)
        port = reactor.listenTCP(utils.get_port(), factory)
        print('TCP Port %s.' % (port.getHost()))

        factory = WebSocketServerFactory()
        factory.protocol = MyServerProtocol
        port = reactor.listenTCP(5506, factory)
        print('WebSocket Port %s.' % (port.getHost()))

        reactor.run()
    except:
        print('INIT error')