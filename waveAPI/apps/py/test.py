#!/usr/bin/python
import utils
utils.setSystemSettings()

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=55558, help="run on the given port", type=int)


class Hello(tornado.web.RequestHandler):

    def open(self):
        print "Hello.open"



    def get(self):
        print "Hello.get"
        self.write("HTTP Hello, world")
        #self.clear()
        #self.set_status(400)
        #self.finish("<html><body>My custom body</body></html>")
        self.write("<br><br>>")

    def on_message(self, message):
        print "Hello.on_message"
        pass

    def on_close(self):
        print "Hello.on_close"
        pass


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print "MainHandler.get"
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
