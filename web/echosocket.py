import logging
import tornado.websocket

log = logging.getLogger('echosocket')

class EchoSocket(tornado.websocket.WebSocketHandler):
    def allow_draft76(self):
        return True

    def initialize(self, app):
        self.app = app

    def open(self):
        log.info('new connection')

    def on_message(self, message):
        log.info('message: %r', message)
        self.write_message(message)

    def on_close(self):
        log.info('connection closed')

