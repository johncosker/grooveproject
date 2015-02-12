#!/usr/bin/python
import utils
import json
from wv_playerManager import playerManager
from parse_cmd import main_parser
from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.resource import Resource
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet import reactor, threads, ssl
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import logging
from dbMgr.usersMgr import userMgr
useSSL = False


class tcp_CmdProtocol(Protocol):
    def dataReceived(self, payload):
        try:
            response = parser.parse_message(json.loads(payload))
            self.transport.write(json.dumps(response))
            self.transport.write('\n')

        except Exception as exc:
            print str(exc)
            logging.info(str(exc))
            self.transport.write(json.dumps({'error': True,
                                             'errorStr': exc.args[0]}))
            self.transport.write('\n')

    def write(self, string):
        self.transport.write(string)

    def err(self, string):
        self.transport.write('Error thing')


class tcp_Factory(ServerFactory):
    protocol = tcp_CmdProtocol

    def __init__(self, parser):
        self.parser= parser

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

        payload = json.loads(payload)
        print payload['user']
        auth = userMgr(payload)
        if not auth.checkUser():
            self.sendMessage((json.dumps({'type': 'Message',
                                          'Message': 'Received'})),
                             False)
            return

        cmd_parse = main_parser()
        response = parser.parse_message(payload)
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

    def __init__(self, parser):
        WebSocketServerFactory.__init__(self)
        self.parser= parser

# __init__
if __name__ == '__main__':
    # Website hosting
    print utils.webDir + 'veiws'
    root = Resource()
    root.putChild('WavePortal', File(utils.webDir + 'views/'))
    root.putChild('3rd_party', File(utils.webDir + '3rd_party'))
    root.putChild('htdocs', File(utils.webDir + 'htdocs'))
    #resource = File(utils.webDir + 'views/index.html')
    port = reactor.listenTCP(80, Site(root))
    print('Web Hosting Port: %s.' % (port.getHost()))



    # CMD listener factorys
    parser = main_parser()
    factory = tcp_Factory(parser)

    if useSSL:
        contextFactory = ssl.DefaultOpenSSLContextFactory(utils.keyDir + 'server.key',
                                                          utils.keyDir + 'server.crt')
        port = reactor.listenSSL(5505, factory, contextFactory)
    else:
        port = reactor.listenTCP(5505, factory)
    print('TCP Port:         %s.' % (port.getHost()))

    factory = webSockect_Factory(parser)

    if useSSL:
        port = reactor.listenSSL(5506, factory, contextFactory)
    else:
        port = reactor.listenTCP(5506, factory)

    print('WebSocket Port:   %s.' % (port.getHost()))
    reactor.run()
