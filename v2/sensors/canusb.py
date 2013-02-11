import trip

class CanUsb(Sensor):
    def __init__(self, name=None, bitrate=None, flags=None):
        import pycanusb
        self.canusb = pycanusb.open(name, bitrate, flags, self.read_callback)

    def read_callback(self, frame):

        ioloop.add_callback(lambda:self.publish(
            'can.%03x' % frame.id,
            frame.timestamp, frame))


import struct
class CanUSBLog(log.TimeSeriesStruct):
    handles = 'can.[0-9a-f]{3}$'

    format = '!dHBB8B'
    size = struct.calcsize(format)

    def from_object(frame):
        return frame.tostring()

    def from_string(string):
        return Frame


