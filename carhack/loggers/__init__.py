
class TimeSeriesInterface(object):
  _loggers = {}
  class __metaclass__(type):
    def __init__(cls, name, bases, dict):
      type.__init__(cls, name, bases, dict)
      if bases != (object,):
        TimeSeriesInterface._loggers[name] = cls
        cls.name = name

  @staticmethod
  def get_by_name(name):
    return TimeSeriesInterface._loggers[name]

  def open(self, basename, fname):
    raise NotImplementedError

  def files(self):
    raise NotImplementedError

  def manifest(self):
    return {
      'logger_name': self.name,
      'fname': self.fname,
      'files': self.files(),
    }

  def close(self):
    raise NotImplementedError

  def __del__(self):
    self.close()

  def __len__(self):
    raise NotImplementedError

  def append(self, ts, value):
    raise NotImplementedError

  def get(self, i):
    raise NotImplementedError

  def __getitem__(self, i):
    return self.get(i)

  def get_range(self, start, end):
    '''
    return array of (timestamp, value) enties
    where the first timestamp is <= start
    and the last timestamp is < end
    '''
    raise NotImplementedError


def get_logger_by_name(name):
  return TimeSeriesInterface.get_by_name(name)

import re
def guess_logger(series_name, example):
  '''Find a good logger for the data we have'''

  if re.match('^canusb.can.*', series_name):
    return CANLog

  if type(example) is int:
    return IntLog

  if type(example) is float:
    return DoubleLog

  # really slow and inefficient
  return SQLiteLogger



from sqlite_logger import SQLiteLog
from struct_logger import CANLog, DoubleLog, IntLog


