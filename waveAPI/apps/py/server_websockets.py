#!/usr/bin/python
import utils
import signal, sys
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer


class web_handler(WebSocket):
    def handleMessage(self):
        if self.data is None:
            self.data = ''
        try:
            self.sendMessage(str(self.data))
        except Exception as n:
            print(n)

    def handleConnected(self):
        print(self.address, 'connected')
        pass

    def handleClose(self):
        print(self.address, 'disconnected')
        pass


if __name__ == "__main__":
    def close_sig_handler(signal, frame):
      server.close()
      sys.exit()

    server = SimpleWebSocketServer('', 55558, web_handler)
    signal.signal(signal.SIGINT, close_sig_handler)
    server.serveforever()
