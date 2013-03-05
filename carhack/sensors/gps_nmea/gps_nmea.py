
import serial
from pynmea.streamer import NMEAStreamer

class NMEA(object):
  def __init__(self, fname='\\\\.\\COM6'):
    self.com = serial.Serial(fname)
    self.streamer = NMEAStreamer(self.com)

  def close(self):
    self.com.close()

  def __iter__(self):
    return self

  def __next__(self):
    if self.com is None:
      raise StopIteration

    next = self.streamer.get_objects()
    if not next:
      raise StopIteration

    return next

if __name__ == '__main__':
  for data in NMEA():
    print data
