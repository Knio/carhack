import os
import re
import time
import json
from collections import defaultdict

import loggers
import sensors

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

  def j(self, *args):
    return os.path.join(self.path, *args)

  def to_json(self):
    return dict(
      tid=self.tid,
      name=self.name,

      live=self.live,

      ts_start=self.ts_start,
      ts_end=self.ts_end,

      sensors=sorted(self.sensors.keys()),
      processors=sorted(self.processors.keys()),
      series=sorted(self.series.keys()),
    )


import heapq
def series_reader(series):
  next = []
  for name in series:
    s = series[name]
    if len(s):
      timestamp, value = s[0]
      heapq.heappush(next, (timestamp, value, 0, name))

  while next:
    timestamp, value, i, name = heapq.heappop(next)
    s = series[name]
    _i = i + 1
    if i < len(s):
      _timestamp, _value = s[_i]
      heapq.heappush(next, (_timestamp, _value, _i, name))
    yield name, (timestamp, value)


class LoggedTrip(Trip):
  live = False
  def __init__(self, tid, path):
    name = tid
    super(LoggedTrip, self).__init__(tid, path)
    self.config = json.load(open(self.j('CONFIG'), 'rb'))
    self.ts_start, self.ts_end = self.config['time_interval']
    self.load_logs()

  def load_logs(self):
    self.sensors = {i:None for i in self.config['sensors']}
    self.processors = {i:None for i in self.config['processors']}

    d1 = self.j('primary')
    d2 = self.j('secondary')
    if not os.path.isdir(d2):
      os.mkdir(d2)

    for name, filename in self.config['series'].iteritems():
      ns = name.split('.')[0]
      if ns not in self.config['sensors']: continue
      series = loggers.get_logger(name)()
      series.open(filename)
      self.series[name] = series

  def recalculate(self):
    pub = Publisher()
    reader = LogReader(self.series.values())

    # TODO setup processors
    raise NotImplementedError

    for name, (timestamp, value) in series_reader(self.series):
      pub.fire(name, timestamp, value)


class LiveTrip(Trip, Publisher):
  live = True
  def __init__(self, tid, path):
    super(LiveTrip, self).__init__(tid, path, 'Current trip')
    log.info('Initializing current trip %s' % tid)
    if not os.path.isdir(path):
      os.mkdir(path)
    self.config = dict(sensors=[], processors=[], series={})
    self.ts_start = time.time()
    self.init_sensors()

  def write_manifest(self):
    with open(self.j('CONFIG'), 'wb') as f:
      json.dump(self.config, f, indent=1)

  def close(self):
    self.ts_end = time.time()
    self.config['time_interval'] = (self.ts_start, self.ts_end)
    self.write_manifest()
    for s in self.series.itervalues():
      s.close()

  def init_sensors(self):
    d1 = self.j('primary')
    if not os.path.isdir(d1):
      os.mkdir(d1)

    sensor_names = app.config.items('sensors')
    for sensor_name, value in sensor_names:
      if not app.config.getboolean('sensors', sensor_name):
        continue
      self.init_sensor(sensor_name)

  def init_sensor(self, name):
      self.config['sensors'].append(name)
      log.info('Loading sensor %s' % name)
      sensor = sensors.get_sensor(name)()
      self.sensors[name] = sensor

  def publish(self, name, timestamp, value):
    if not name in self.series:
      series = loggers.get_logger(name)()
      ns = name.split('.')[0]
      if ns in self.sensors:
        path = 'primary'
      if ns in self.processors:
        path = 'secondary'
      filename = self.j(path, '%s.dat' % name)
      series.open(filename)
      self.series[name] = series
      self.config['series'][name] = filename
    self.series[name].append(timestamp, value)
    self.fire(name, timestamp, value)


from carapp import app, log
