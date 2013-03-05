import time
import logging

import tornado.ioloop

import carhack.sensors

log = logging.getLogger('nmea')
ioloop = tornado.ioloop.IOLoop.instance()

import serial
import threading

class SerialNMEA(carhack.sensors.Sensor):
  def __init__(self, filename='\\\\.\\COM6'):
    self.filename = filename
    self.timeout = 5.
    self.thread = threading.Thread(target=self.run)
    self.thread.daemon = True
    self.running = True
    self.thread.start()

  def close(self):
    self.running = False

  def run(self):
    com = None
    buff = ''
    while self.running:
      if com is None:
        try:
          com = serial.Serial(self.filename, timeout=self.timeout)
          buff = ''
        except serial.SerialException:
          log.debug('could not connect to %s' % self.filename)
          time.sleep(self.timeout)
          continue

      data = com.read(16)
      if not data:
        log.debug('lost connection')
        com.close()
        com = None
        continue

      now = time.time()
      lines = (buff + data).split('\r\n')
      buff = lines.pop()
      for line in lines:
        self.pub(now, line)
        now += 0.001

    if com:
      com.close()

  def pub(self, ts, line):
    log.debug("%10.3f %s" % (ts, line))
    ioloop.add_callback(lambda:self.publish(
      'nmea_string', ts, line))


sensor = SerialNMEA
