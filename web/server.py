import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import index

class WSHandler(tornado.websocket.WebSocketHandler):
    def allow_draft76(self):
        return True

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

class WebcamHandler(tornado.web.RequestHandler):
    jpeg = None

    @classmethod
    def start(cls):
        import time
        import threading
        from cStringIO import StringIO
        from VideoCapture import Device
        
        cam = Device()
        def loop():
            while 1:
                file = StringIO()
                image = cam.getImage(1)
                image.save(file, 'jpeg')
                cls.jpeg = file.getvalue()
                # TODO log image?
                time.sleep(0.1)

        thread = threading.Thread(target=loop)
        thread.start()

    def get(self):
        self.set_header('Cache-Control', 'no-cache')
        if not self.jpeg:
            self.set_status(503)
            self.write('camera offline, please try again later')
            return
        self.set_header('Content-Type', 'image/jpeg')
        self.write(self.jpeg)

WebcamHandler.start()

def main():

    application = tornado.web.Application([
        (r'/static/(.*)',   tornado.web.StaticFileHandler, dict(path='static')),
        (r'/cam.jpg',       WebcamHandler),
        (r'/ws',            WSHandler),
        (r'/',              MainHandler),
    ])

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8001)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
