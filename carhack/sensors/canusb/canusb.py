import tornado.ioloop

import carhack.sensors

ioloop = tornado.ioloop.IOLoop.instance()


class CanUsb(carhack.sensors.Sensor):
  def __init__(self, name=None, bitrate='500', flags=None):
    import pycanusb
    self.canusb = pycanusb.open(name, bitrate, flags, self.read_callback)
    # self.obd2 = OBD2Scanner(self)

  def read_callback(self, frame):
    ioloop.add_callback(lambda:self.publish(
      'can.%03x' % frame.id,
      frame.timestamp, frame.tojson()))

  def close(self):
    self.canusb = None


class OBD2Scanner(object):
  def __init__(self, canusb):
    pass


