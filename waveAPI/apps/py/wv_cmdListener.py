#!/usr/bin/python
import utils
import json
from wv_playerManager import start_playerManager
from parse_cmd import main_parser
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet import reactor, threads, ssl
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from dbMgr.usersMgr import userMgr
useSSL = False


class tcp_CmdProtocol(Protocol):
    def connectionMade(self, payload):
        pass

    def dataReceived(self, payload):
        try:
            cmd_parse = main_parser(player_q)
            response = cmd_parse.parse_message(json.loads(payload))
            self.transport.write(json.dumps(response))
            self.transport.write('\n')

        except  Exception as exc:
            self.transport.write(json.dumps({'error': True,
                                             'errorStr': exc.args[0]}))
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
    def onConnect(self, request):
        pass

    def onOpen(self):
        pass

    def onMessage(self, payload, isBinary):
        print 'onMEssage'
        if payload == 'INIT_CONN':
            self.sendMessage((json.dumps({'type': 'Message',
                                          'Message': 'Received'})),
                             False)
            return
        #try:webSockect_Factory
        print "hi"
        payload = json.loads(payload)
        print payload['user']
        auth = userMgr(payload['user'])
        if not auth.checkUser():
            self.sendMessage((json.dumps({'type': 'Message',
                                          'Message': 'Received'})),
                             False)
            return

        cmd_parse = main_parser(player_q)
        response = cmd_parse.parse_message(payload)
        self.sendMessage((json.dumps(response)), False)
        '''
        except  Exception as exc:
            self.sendMessage((json.dumps({'error': True,
                                          'errorStr': exc.args[0]})),
                             False)
        '''
    def onClose(self, wasClean, code, reason):
        pass


class webSockect_Factory(WebSocketServerFactory):
    protocol = webSockect_CmdProtocol

    def __init__(self, player_q):
        WebSocketServerFactory.__init__(self)
        self.player_q = player_q


# __init__
if __name__ == '__main__':
    player_q = start_playerManager()
    factory = tcp_Factory(player_q)

    if useSSL:
        contextFactory = ssl.DefaultOpenSSLContextFactory(utils.keyDir + '/server.key',
                                                          utils.keyDir + '/server.crt')
        port = reactor.listenSSL(5505, factory, contextFactory)
    else:
        port = reactor.listenTCP(5505, factory)
    print('TCP Port %s.' % (port.getHost()))

    factory = webSockect_Factory(player_q)

    if useSSL:
        port = reactor.listenSSL(5506, factory, contextFactory)
    else:
        port = reactor.listenTCP(5506, factory)

    print('WebSocket Port %s.' % (port.getHost()))
    reactor.run()
