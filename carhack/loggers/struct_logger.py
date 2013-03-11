import os
import mmap
import time
import struct
from collections import OrderedDict

from carhack.loggers import TimeSeriesInterface

class StructLog(TimeSeriesInterface):
  '''
  On-disk array of struct objects.
  Abstract class. Concrete classes must implement:

  * item_size
  * encode
  * decode

  '''
  def __init__(self):
    self.file = None
    super(StructLog, self).__init__()
    self.format = '@d%ds' % self.item_size
    self.size = struct.calcsize(self.format)

  def decode(self, bytes):
    raise NotImplementedError

  def encode(self, obj):
    raise NotImplementedError

  def files(self):
    return [self.fname]

  def open(self, basename, fname):
    self.fname = fname
    fullname = os.path.join(basename, fname)
    self.file = open(fullname, 'a+b')
    self.file.seek(0, 2)
    l = self.file.tell()
    self.file_len = l / self.size
    if l == 0:
      # can't mmap empty file, so put some fake data in it
      self.file.write('X' * self.size)
      self.file.flush()
      l = self.size
    self.map = mmap.mmap(self.file.fileno(), l)

    self.buffer = []
    self.tscache = OrderedDict()

  def __len__(self):
    return self.file_len + len(self.buffer)

  def get_file(self, index):
    ts, bytes = struct.unpack_from(
      self.format, self.map, index * self.size)

    return ts, self.decode(bytes)

  def get(self, i):
    if i >= self.file_len:
      if i >= len(self):
        raise IndexError
      return self.buffer[i - self.file_len]
    else:
      return self.get_file(i)

  __getitem__ = get

  def flush(self, andfile=False):
    if len(self.buffer):
      self.map.resize((self.file_len + len(self.buffer)) * self.size)
    for timestamp, obj in self.buffer:
      data = self.encode(obj)
      struct.pack_into(self.format,
        self.map, (self.file_len * self.size),
        timestamp, data)
      self.file_len += 1

    self.buffer = []
    if andfile:
      self.map.flush()

  def find_index(self, ts):
    '''
    Finds the highest index with timestamp <= ts
    '''
    s = 0
    e = len(self)

    while (e - s) > 1:
      m = (s + e) / 2

      timestamp = self.tscache.get(m)
      if not timestamp:
        timestamp, data = self.get(m)
        self.tscache[m] = timestamp
      else:
        self.tscache.pop(m)
      self.tscache[m] = timestamp

      if timestamp > ts:
        e = m
      else:
        s = m

    while len(self.tscache) > len(self) / 8:
      self.tscache.popitem()

    return s

  def get_range(self, begin_ts, end_ts=None):
    end_ts = end_ts or 1e10
    s = self.find_index(begin_ts)
    rows = []
    while s < len(self):
        row = self[s]
        if row[0] >= end_ts:
            break
        rows.append(row)
        s += 1

    return rows

  def append(self, timestamp, obj):
    self.buffer.append((timestamp, obj))
    if len(self.buffer) > 1024:
      self.flush()

  def close(self):
    if self.file:
      self.flush(True)
      self.map.close()
      self.file.close()
      self.file = None


class CANLog(StructLog):
  can_struct = struct.Struct('!dHBB8B')
  item_size = can_struct.size

  def encode(self, can):
    data = [0] * 8
    d = can['data']
    data[0:len(d)] = d
    return self.can_struct.pack(
      can['timestamp'],
      can['id'],
      can['flags'],
      can['len'],
      *data)

  def decode(self, bytes):
    d = self.can_struct.unpack(bytes)
    return {
      'timestamp':  d[0],
      'id':         d[1],
      'flags':      d[2],
      'len':        d[3],
      'data':       d[4:4+d[3]],
    }


class ScalarLog(StructLog):
  def encode(self, obj):
    return struct.pack(self.item, obj)
  def decode(self, bytes):
    return struct.unpack(self.item, bytes)[0]

class DoubleLog(ScalarLog):
  item = '!d'
  item_size = struct.calcsize(item)


class IntLog(ScalarLog):
  item = '!q'
  item_size = struct.calcsize(item)


def test():
  s = struct.Struct('!H')

  class TestStructTimeSeries(StructLog):
    name_pattern = '$^'
    item_size = s.size

    def encode(self, obj):
      return s.pack(obj)

    def decode(self, string):
      return s.unpack(string)[0]

  time_series.test(TestStructTimeSeries, iter(xrange(50, 100)))


if __name__ == '__main__':
  test()
