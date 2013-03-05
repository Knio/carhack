import tornado.ioloop

import carhack.sensors

ioloop = tornado.ioloop.IOLoop.instance()

import serial
from pynmea.streamer import NMEAStreamer

class GPSNMEA(carhack.sensors.Sensor):
  def __init__(self):
    self.com = serial.Serial('\\\\.\\COM6')


  def read_callback(self, frame):

    ioloop.add_callback(lambda:self.publish(
      'can.%03x' % frame.id,
      frame.timestamp, frame.tojson()))


sensor = GPSNMEA
