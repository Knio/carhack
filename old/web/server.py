import logging

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import index

class WSHandler(tornado.websocket.WebSocketHandler):
    def allow_draft76(self):
        return True

    def initialize(self, app):
        self.app = app

    def open(self):
        logging.getLogger('websocket').info('new connection')

    def on_message(self, message):
        logging.getLogger('websocket').info('message: %r', message)

        self.write_message(message)

        # def read(frame):
        #     self.write_message(frame.tojson())

        # self.read =
        # self.app.can.subscribe()



    def on_close(self):
        logging.getLogger('websocket').info('connection closed')

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, app):
        self.app = app

    def get(self):
        self.write(unicode(index.main(self)))

class WebcamHandler(tornado.web.RequestHandler):
    def initialize(self, app):
        self.app = app

    def get(self):
        self.set_header('Cache-Control', 'no-cache')
        data = app.webcam.get_image()
        if not data:
            self.set_status(503)
            self.write('camera offline, please try again later')
            return
        self.set_header('Content-Type', 'image/jpeg')
        self.write(data)


class TornadoServer(object):
    def __init__(self, carapp):

        self.tornadoapp = tornado.web.Application([
            (r'/static/(.*)',   tornado.web.StaticFileHandler, dict(path='static')),
            (r'/cam.jpg',       WebcamHandler),
            (r'/ws',            WSHandler, dict(app=carapp)),
            (r'/',              MainHandler, dict(app=carapp)),
        ])

        self.http_server = tornado.httpserver.HTTPServer(self.tornadoapp)
        self.http_server.listen(8001)

    def run(self):
        # block forever
        tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    server = TornadoServer(None)
    server.start()
