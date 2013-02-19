import os
from collections import defaultdict

import loggers

class Publisher(object):
  def __init__(self):
    self.subscribers = defaultdict(list)

  def subscribe(self, name, subscriber):
    self.subscribers[name].append(subscriber)

  def fire(self, name, timestamp, value):
    for subscriber in self.subscribers[name]:
      subscriber(timestamp, value)

    for subscriber in self.subscribers[None]:
      subscriber(timestamp, value)


class Trip(object):
  def __init__(self, tid, path, name=None):
    super(Trip, self).__init__()
    self.tid = tid
    self.path = path
    self.name = name or tid

    self.ts_start = 0
    self.ts_end = 0

    self.sensors = {}
    self.processors = {}

    self.series = {}

  def get_sensors(self):
    pass

  def j(self, *args):
    return os.path.join(self.path, *args)


class LoggedTrip(Trip):
  def __init__(self, tid, path):
    name = tid
    super(LoggedTrip, self).__init__(tid, path)
    self.load_logs()

  def load_logs(self):
    d1 = self.j('primary')
    if not os.path.isdir(d1):
      os.mkdir(d1)
    d2 = self.j('secondary')
    if not os.path.isdir(d2):
      os.mkdir(d2)

    raise NotImplementedError

  def recalculate(self):
    pub = Publisher()
    raise NotImplementedError

  def get_sensors(self):
    sensors = os.listdir(self.j('primary'))

  def get_processors(self):
    sensors = os.listdir(self.j('secondary'))


class LiveTrip(Trip, Publisher):
  def __init__(self, tid, path):
    super(LiveTrip, self).__init__(tid, path, 'Current trip')
    log.info('Initializing current trip %s' % tid)
    if not os.path.isdir(path):
      os.mkdir(path)

    self.init_sensors()

  def init_sensors(self):
    sensor_names = app.config.items('sensors')
    log.info(repr(sensor_names))
    for sensor_name, value in sensor_names:
      if not app.config.getboolean('sensors', sensor_name):
        continue
      self.init_sensor(sensor_name)

  def init_sensor(self, name):
      log.info('Loading sensor %s' % name)
      sensors = __import__('sensors.%s' % name, globals(), level=0)
      module = getattr(sensors, name)
      sensor = module.sensor()
      self.sensors[name] = sensor

  def publish(self, name, timestamp, value):
    if not name in self.series:
      series = loggers.TimeSeriesInterface.get_handler(name)()
      series.open(self.j('%s.dat' % name))
      self.series[name] = series
    self.series[name].append(timestamp, value)
    self.fire(name, timestamp, value)

import heapq
class LogReader(object):
  def __init__(self, logs=None):
    self.logs = []
    self.next = []
    for l in logs:
      self.add_log(l)


  def add_log(self, log):
    self.logs.append(log)
    if len(log):
      l = log
      i = 0
      v = l[0]
      d = v[0]
      heapq.heappush(self.next, (d, v, i, l))

  def next(self):
    d, v, i, l = heapq.heappop(self.next)
    _i = i + 1
    if i < len(l):
      _v = l[_i]
      _d = _v[0]
      heapq.heappush(self.next, (_d, _v, _i, l))
    return v

from carapp import app, log
