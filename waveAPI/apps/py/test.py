#!/usr/bin/python
#import utils


from ws4py.client import WebSocketBaseClient
from ws4py.manager import WebSocketManager
from ws4py import format_addresses, configure_logger

logger = configure_logger()

m = WebSocketManager()
print("0")
class EchoClient(WebSocketBaseClient):
    def handshake_ok(self):
        logger.info("Opening %s" % format_addresses(self))
        m.add(self)

    def received_message(self, msg):
        logger.info(str(msg))

if __name__ == '__main__':
    import time

    try:
        m.start()
        for i in range(2000):
            client = EchoClient('ws://localhost:55558/ws')
            client.connect()

        logger.info("%d clients are connected" % i)

        while True:
            for ws in m.websockets.itervalues():
                if not ws.terminated:
                   break
            else:
                break
            time.sleep(3)
    except KeyboardInterrupt:
        m.close_all()
        m.stop()
        m.join()




"""
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print("get")
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(55558)
    tornado.ioloop.IOLoop.instance().start()


"""

"""
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=55558, help="run on the given port", type=int)


class Hello(tornado.web.RequestHandler):

    def open(self):
        print("Hello.open")



    def get(self):
        print("Hello.get")
        self.write("HTTP Hello, world")

    def on_message(self, message):
        print("Hello.on_message")
        pass

    def on_close(self):
        print("Hello.on_close")
        pass


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print("MainHandler.get")
        self.write("Hello, world")


def main():
    #tornado.options.parse_command_line()
    application = tornado.web.Application([(r"/", MainHandler),
                                           (r"/websocket", Hello),])
    application.listen(55558)
    #http_server = tornado.httpserver.HTTPServer(application)
    #http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
"""