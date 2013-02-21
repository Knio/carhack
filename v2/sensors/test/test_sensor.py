import time
import random
import threading
import tornado.ioloop

import sensor

ioloop = tornado.ioloop.IOLoop.instance()


class TestSensor(sensor.Sensor):
  def __init__(self):
    t = threading.Thread(target=self.go)
    t.daemon = True
    t.start()

  def iter(self):
    v = 0.0
    while 1:
      yield v
      v += (random.random() - 0.5)

  def go(self):
    for value in self.iter():
      time.sleep(0.1)
      ioloop.add_callback(lambda:
        self.publish('random1', time.time(), value))

