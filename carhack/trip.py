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


def normpath(x):
  return x.replace('\\','/')

class Publisher(object):
  def __init__(self):
    self.subscribers = defaultdict(list)

  def subscribe(self, name, subscriber):
    self.subscribers[name].append(subscriber)

  def unsubscribe(self, name, subscriber):
    self.subscribers[name].remove(subscriber)

  def fire(self, name, ts, value):
    for subscriber in self.subscribers[name]:
      subscriber(ts, value)


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
    args = map(normpath, args)
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

  def write_series(self, name, ts, value):
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
      self.config['series'][name] = normpath(filename)
    self.series[name].append(ts, value)


import heapq
def series_reader(series):
  next = []
  for name in series:
    s = series[name]
    if len(s):
      ts, value = s[0]
      heapq.heappush(next, (ts, value, 0, name))

  while next:
    ts, value, i, name = heapq.heappop(next)
    s = series[name]
    _i = i + 1
    if _i < len(s):
      _timestamp, _value = s[_i]
      heapq.heappush(next, (_timestamp, _value, _i, name))
    yield name, (ts, value)


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
      fname = self.j(filename)
      if not os.path.isfile(fname):
        log.info('log file %s does not exist - skipping' % fname)
        continue
      series = loggers.get_logger(name)()
      series.open(fname)
      self.series[name] = series

  def recalculate(self):
    log.info('recalculating trip %s' % self.tid)
    pub = Publisher()

    # delete old logs
    for name, filename in self.config['series'].items():
      print filename
      if name not in self.series:
        continue
      if filename.startswith('secondary'):
        self.series[name].close()
        del self.series[name]
        del self.config['series'][name]
        os.remove(self.j(filename))


    d2 = self.j('secondary')
    if not os.path.isdir(d2):
      os.mkdir(d2)
    assert os.listdir(d2) == []

    self.write_manifest()

    def publish(name, ts, value):
      log.debug("%10.3f %s %r" % (ts, name, value))
      self.write_series(name, ts, value)
      pub.fire(name, ts, value)

    pub.publish = publish

    processor_names = [name for (name, value) in app.config.items('processors')
      if app.config.getboolean('processors', name)]

    self.processors = {}
    self.config['processors'] = processor_names

    # TODO wipe series manifest??
    for processor_name in processor_names:
      log.info('loading processor %s' % processor_name)
      processor = processors.get_processor(processor_name)(pub)
      self.processors[processor_name] = processor

    try:
      for name, (ts, value) in series_reader(self.series):
        pub.fire(name, ts, value)

    finally:
      for processor in self.processors.itervalues():
        processor.close()
      for series in self.series.itervalues():
        series.close()
      self.write_manifest()

    self.load_logs()


class LiveTrip(Trip, Publisher):
  live = True
  def __init__(self, tid, path):
    super(LiveTrip, self).__init__(tid, path, 'Current trip')
    log.info('Initializing current trip %s' % tid)
    if not os.path.isdir(path):
      os.mkdir(path)
    self.ts_start = time.time()
    self.init_sensors()
    self.init_processors()

  def close(self):
    self.ts_end = time.time()
    self.config['time_interval'] = (self.ts_start, self.ts_end)
    self.write_manifest()

    for sensor in self.sensors.itervalues():
      sensor.close()
    for processor in self.processors.itervalues():
      processor.close()
    for series in self.series.itervalues():
      series.close()

  def init_processors(self):
    d2 = self.j('secondary')
    if not os.path.isdir(d2):
      os.mkdir(d2)

    processor_names = [name for (name, value) in app.config.items('processors')
      if app.config.getboolean('processors', name)]

    self.config['processors'] = processor_names
    for name in processor_names:
      log.info('loading processor %s' % name)
      processor = processors.get_processor(name)(self)
      self.processors[name] = processor

  def init_sensors(self):
    d1 = self.j('primary')
    if not os.path.isdir(d1):
      os.mkdir(d1)

    sensor_names = [name for (name, value) in app.config.items('sensors')
      if app.config.getboolean('sensors', name)]

    self.config['sensors'] = sensor_names
    for name in sensor_names:
      log.info('Loading sensor %s' % name)
      sensor = sensors.get_sensor(name)()
      self.sensors[name] = sensor

  def publish(self, name, ts, value):
    # log.debug("%10.3f %s %r" % (ts, name, value))
    self.write_series(name, ts, value)
    self.fire(name, ts, value)


from carapp import app, log
