import os
import re
import time
import json
import shutil
from collections import defaultdict

import loggers
import sensors
import processors

CONFIG_NAME = 'LOG_CONFIG'

class Publisher(object):
  def __init__(self):
    self.subscribers = defaultdict(list)

  def subscribe(self, name, subscriber):
    self.subscribers[name].append(subscriber)

  def unsubscribe(self, name, subscriber):
    self.subscribers[name].remove(subscriber)

  def fire(self, name, timestamp, value):
    for subscriber in self.subscribers[name]:
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

    self.config = dict(sensors=[], processors=[], series={})

  def j(self, *args):
    return os.path.join(self.path, *args)

  def write_manifest(self):
    with open(self.j(CONFIG_NAME), 'wb') as f:
      json.dump(self.config, f, indent=1)

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

  def write_series(self, name, timestamp, value):
    if not name in self.series:
      series = loggers.get_logger(name)()
      ns = name.split('.')[0]
      if ns in self.sensors:
        path = 'primary'
      elif ns in self.processors:
        path = 'secondary'
      else:
        raise Exception
      filename = os.path.join(path, '%s.dat' % name)
      series.open(self.j(filename))
      self.series[name] = series
      self.config['series'][name] = filename
    self.series[name].append(timestamp, value)


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
    if _i < len(s):
      _timestamp, _value = s[_i]
      heapq.heappush(next, (_timestamp, _value, _i, name))
    yield name, (timestamp, value)


class LoggedTrip(Trip):
  live = False
  def __init__(self, tid, path):
    name = tid
    super(LoggedTrip, self).__init__(tid, path)
    self.config = json.load(open(self.j(CONFIG_NAME), 'rb'))
    self.ts_start, self.ts_end = self.config['time_interval']
    self.load_logs()

  def load_logs(self):
    self.sensors = {i:None for i in self.config['sensors']}
    self.processors = {i:None for i in self.config['processors']}

    for name, filename in self.config['series'].iteritems():
      ns = name.split('.')[0]
      if ns not in self.config['sensors']: continue
      series = loggers.get_logger(name)()
      series.open(self.j(filename))
      self.series[name] = series

  def recalculate(self):
    pub = Publisher()

    # delete old logs
    d2 = self.j('secondary')
    for name, filename in self.config['series'].items():
      if filename.startswith(d2):
        self.series[name].close()
        del self.series[name]
        del self.config[name]
        os.remove(filename)

    if not os.path.isdir(d2):
      os.mkdir(d2)
    assert os.listdir(d2) == []

    def publish(name, ts, value):
      self.write_series(name, ts, values)
      pub.fire(name, ts, value)

    pub.publish = publish

    processor_names = [name for (name, value) in app.config.items('processors')
      if app.config.getboolean('processors', name)]

    self.processors = {}
    self.config['processors'] = processor_names

    # TODO wipe series manifest??
    for processor_name in processor_names:
      processor = processors.get_processor(processor_name)(pub)
      self.processors[processor_name] = processor

    for name, (ts, value) in series_reader(self.series):
      pub.fire(name, ts, value)

    self.write_manifest()


class LiveTrip(Trip, Publisher):
  live = True
  def __init__(self, tid, path):
    super(LiveTrip, self).__init__(tid, path, 'Current trip')
    log.info('Initializing current trip %s' % tid)
    if not os.path.isdir(path):
      os.mkdir(path)
    self.ts_start = time.time()
    self.init_sensors()

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

  def publish(self, name, ts, value):
    self.write_series(name, ts, value)
    self.fire(name, ts, value)


from carapp import app, log
