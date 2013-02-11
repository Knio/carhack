
import pycanusb

class CanUsb(Sensor):
    def __init__(self, name=None, bitrate=None, flags=None):
        self.canusb = pycanusb.open(name, bitrate, flags, self.callback)

    def callback(self, frame):
        pass
        ioloop.add_callback(lambda:self.publish(frame))
