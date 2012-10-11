import can
import web
import camera

class CarApp(object):
    def __init__(self):

        self.can = can.CAN()
        self.cam = camera.Webcam()

        self.tornado = web.TornadoServer(self)


    def run(self):
        self.tornado.start()


if __name__ == '__main__':
    app = CarApp()
    app.run()
