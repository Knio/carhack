import tornado.ioloop

ioloop = tornado.ioloop.IOLoop.instance()


class CanUsb(Sensor):
    def __init__(self, name=None, bitrate=None, flags=None):
        import pycanusb
        self.canusb = pycanusb.open(name, bitrate, flags, self.read_callback)

    def read_callback(self, frame):

        ioloop.add_callback(lambda:self.publish(
            'can.%03x' % frame.id,
            frame.timestamp, frame))


import pycanusb.Frame
class CanUSBLog(log.TimeSeriesStruct):
    name_pattern = 'can.[0-9a-f]{3}$'
    item_format = pycanusb.Frame.format
    item_size = struct.calcsize(item_format)

    def from_object(frame):
        return frame.tostring()

    def from_string(string):
        return Frame(string)


