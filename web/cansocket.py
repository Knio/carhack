import json
import logging
import tornado.websocket

log = logging.getLogger('cansocket')

class CanSocket(tornado.websocket.WebSocketHandler):
    def allow_draft76(self):
        return True

    def initialize(self, app):
        self.app = app
        self.read = None

    def open(self):
        log.info('new connection')

    def on_message(self, message):
        log.info('message: %r', message)
        msg = json.loads(message)

        def read(frame):
            self.write_message(frame.tojson())

        self.read = read
        self.app.can.subscribe(read, 
            ids=msg.get('ids'), 
            suppress_duplicates=msg.get('suppress_duplicates', False))

    def on_close(self):
        log.info('connection closed')
        if self.read:
            self.app.can.unsubscribe(self.read)
