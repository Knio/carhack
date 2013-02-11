from collections import defaultdict

from app import app, log


class Publisher(object):
  def __init__(self):
    self.subscribers = defaultdict(list)

  def subscriber(self, name, subscriber):
    self.subscribers[name].append(subscriber)

  def fire(self, name, value):
    for subscriber in self.subscribers[name]
      subscriber(value)

    for subscriber in self.subscribers[None]:
      subscriber(value)


class Trip(object):
  def __init__(self, path, tid, name):
    self.tid = tid
    self.name = name
    self.ts_start = 0
    self.ts_end = 0

    self.sensors = []
    self.processors = []

    self.series = []
    self.path = path

  def get_sensors(self):
    pass

  def j(self, *args):
    return os.path.join(self.path, *args)


class LoggedTrip(Trip):
  def __init__(self,  path, tid):
    name = tid
    super(LoggedTrip, self).__init__(path, tid, name)
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


class Livetrip(Trip, Publisher):
  def __init__(self,  path, tid):
    super(Livetrip, self).__init__( path, tid, 'Active Trip')


  def get_sensors(self):
    sensors = app.config.items('sensors')
    log.info(repr(sensors))


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



