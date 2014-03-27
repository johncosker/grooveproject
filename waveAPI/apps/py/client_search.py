#!/usr/bin/env python
import webapp2


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)


"""
import sys
import json
import cgi
import webapp2

from grooveshark import Client

print ("Content-Type: html/text")     # HTML is following
print ("")                            # blank line, end of headers

def parseCmd(msg):
    if len(msg) < 3:
        msg = "''"
    else:
        msg = msg[2:-2]
    return msg
    
class requestHandler(webapp2.RequestHandler)
    def get(self):
        cmd = self.request.get('cmd')
        user = self.request.get('user')
        target = self.request.get('target')
        info = self.request.get('info')
        '''
        cmdRequest = cgi.FieldStorage()
        cmd = parseCmd( str(cmdRequest.getlist('cmd')) )
        user = parseCmd( str(cmdRequest.getlist('user')) )
        target = parseCmd( str(cmdRequest.getlist('target')) )
        info = parseCmd( str(cmdRequest.getlist('info')) )
        '''
        client = Client()
        client.init()
        self.response.write(cmd)
        if cmd == 'search':
            songList=client.search(info, type='Songs')
            returnList = []
            print songList
            for song in songList:
                try:
                    returnList.append({'name'     : song.name,
                                      'artist'    : song.artist.name,
                                      'album'     : song.album.name})
                                      #TODO: ADD song.stream.url

                except:
                    tmp = 1
            
            print 'goodhi'
            sys.stdout.write( json.dump(returnList) )
        else:
            tmp = 1

app = webapp2.WSGIApplication([requestHandler])
    #print cmd
    #sys.stdout.write( "fail" )
    
#print "endhi"

"""