import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import index

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        self.write_message("Hello World")

    def on_message(self, message):
        print 'message received %s' % message
        self.write_message(message)

    def on_close(self):
      print 'connection closed'

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(unicode(index.main(self)))

def main():

    application = tornado.web.Application([
        (r'/ws',            WSHandler),
        (r'/static/(.*)',   tornado.web.StaticFileHandler, dict(path='static')),
        (r'/',              MainHandler),
    ])

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8001)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
