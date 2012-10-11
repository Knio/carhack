import tornado.web

class WebcamHandler(tornado.web.RequestHandler):
    def initialize(self, app):
        self.app = app

    def get(self):
        self.set_header('Cache-Control', 'no-cache')
        data = self.app.cam.get_image()
        if not data:
            self.set_status(503)
            self.write('camera offline, please try again later')
            return
        self.set_header('Content-Type', 'image/jpeg')
        self.write(data)
