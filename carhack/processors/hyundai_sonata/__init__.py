import inspect
import logging

from carhack import app
from carhack.processors import Processor, subscribe

log = logging.getLogger('test_proc')

def unsigned_short(a, b):
  return (a<<8) | b

def signed_short(a, b):
  x = (a << 8) | b
  if (x & 0x8000):
    x -= 0x10000
  return x

def percent(a):
  return 100 * (a / 255.)

def bit(x):
  return int(x != 0)


def wrap(func):
  def f(ts, value):
    return func(ts, *value['data'])
  return f


class HyundaiSonataProcessor(Processor):
  def __init__(self, pub):
    super(HyundaiSonataProcessor, self).__init__(pub)
    for name, method in inspect.getmembers(self):
      if not name.startswith('can_'):
        continue
      pub.subscribe(
        'canusb.can.%s' % name.split('_')[1],
        wrap(method))

  def can_316(self, ts, A, B, C, D, E, F, G, H):
    rpm = unsigned_short(D, C)
    vehicle_speed = G
    self.publish('rpm', ts, rpm)
    self.publish('vehicle_speed', ts, vehicle_speed)

  def can_370(self, ts, A, B, C, D, E, F, G, H):
    gear = {
      0: 0,
      16: 1,
      32: 2,
      48: 3,
      64: 4,
      80: 5,
      96: 6,
      224: -1,
    }.get(C, 255)
    self.publish('6AT', ts, gear)

processor = HyundaiSonataProcessor
