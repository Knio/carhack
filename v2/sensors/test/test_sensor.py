import time
import math
import random
import threading
import tornado.ioloop

import sensor

ioloop = tornado.ioloop.IOLoop.instance()


class TestSensor(sensor.Sensor):
  def __init__(self):
    self.start_thread('random1', self.random1)
    self.start_thread('sin1', self.sin1)

  def start_thread(self, name, gen):
    t = threading.Thread(target=self.go, args=(name, gen,))
    t.daemon = True
    t.start()

  def go(self, name, gen):
    for value in gen():
      time.sleep(0.01)
      ioloop.add_callback(lambda:
        self.publish(name, time.time(), value))

  def random1(self):
    v = 0.0
    while 1:
      yield v
      v += (random.random() - 0.5)

  def sin1(self):
      while 1:
        yield math.sin(time.time())

