import mmap
import time
import struct
from collections import OrderedDict

import time_series

class StructTimeSeries(time_series.TimeSeriesInterface):
  '''
  On-disk array of struct objects.
  Abstract class. Concrete classes must implement:

  * item_size
  * from_string
  * from_object

  '''
  def __init__(self):
    super(StructTimeSeries, self).__init__()
    self.format = '@d%ds' % self.item_size
    self.size = struct.calcsize(self.format)

  def from_bytes(self, bytes):
    raise NotImplementedError

  def from_object(self, obj):
    raise NotImplementedError

  def open(self, fname):
    self.file = open(fname, 'a+b')
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

    return ts, self.from_bytes(bytes)

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
      data = self.from_object(obj)
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

  def get_range(self, begin_ts, end_ts=1e10):
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


def test():
  s = struct.Struct('!H')

  class TestStructTimeSeries(StructTimeSeries):
    name_pattern = '$^'
    item_size = s.size

    def from_object(self, obj):
      return s.pack(obj)

    def from_bytes(self, string):
      return s.unpack(string)[0]

  time_series.test(TestStructTimeSeries, iter(xrange(50, 100)))


if __name__ == '__main__':
  test()
