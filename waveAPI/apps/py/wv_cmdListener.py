#!/usr/bin/python
import utils
import json
from wv_playerManager import start_playerManager
from parse_cmd import main_parser
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet import reactor, threads
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory

class tcp_CmdProtocol(Protocol):
    def connectionMade(self):
        pass

    def dataReceived(self, data):
        cmd_parse = main_parser(player_q)
        response = cmd_parse.parse_message(json.loads(data))
        print response
        self.transport.write(json.dumps(response))
        self.transport.write('\n')

    def write(self, string):
        self.transport.write(string)

    def err(self, string):
        self.transport.write('Error thing')


class tcp_Factory(ServerFactory):
    protocol = tcp_CmdProtocol

    def __init__(self, player_q):
        self.player_q = player_q


class webSockect_CmdProtocol(WebSocketServerProtocol):
    def connectionMade(self):
        pass

    def dataReceived(self, data):
        cmd_parse = main_parser(player_q)
        response = cmd_parse.parse_message(json.loads(data))
        self.transport.write(json.dumps(response))
        self.transport.write('\n')

    def write(self, string):
        self.transport.write(string)

    def err(self, string):
        self.transport.write('Error thing')

        
class webSockect_Factory(WebSocketServerFactory):
    protocol = webSockect_CmdProtocol

    def __init__(self, player_q):
        self.player_q = player_q

# __init__
if __name__ == '__main__':
    player_q = start_playerManager()

    factory = tcp_Factory(player_q)
    port = reactor.listenTCP(utils.get_port(), factory)
    print('TCP Port %s.' % (port.getHost()))

    factory = webSockect_Factory(player_q)
    port = reactor.listenTCP(5506, factory)
    print('WebSocket Port %s.' % (port.getHost()))

    reactor.run()