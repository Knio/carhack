

import re

class TimeSeriesInterface(object):
    _handlers = []
    class __metaclass__(type):
        def __init__(cls, name, bases, dict):
            type.__init__(cls, name, bases, dict)
            if bases == (object,):
                return
            pattern = cls.handles
            TimeSeriesInterface._handlers.append((pattern, cls))

    @staticmethod
    def get(name):
        for pattern, cls in TimeSeriesInterface._handlers:
            if re.match(pattern, name):
                return cls

    def open(self):
        pass

    def close(self):
        pass

    def __len__(self):
        pass

    def append(self, ts, value):
        pass

    def get(self, i):
        pass

    def __getitem__(self, i):
        return self.get(i)

    def get_range(self, start, end):
        pass



import mmap
import time
import struct
from collections import OrderedDict

class TimeSeriesStruct(TimeSeriesInterface):
    '''
    On-disk array of struct objects
    '''
    def __init__(self, name, format, basename=None):
        super(TimeSeries, self).__init__()
        self.format = '@d' + format
        self.item_size = struct.calcsize(self.format)


    def open(self):
        fname = name + '.log'
        if basename:
            fname = basename + '.' + name
        self.file = open(fname, 'a+b')
        l = self.file.tell()
        self.file_len = l / self.item_size
        if l == 0:
            # can't mmap empty file
            self.file.write('X' * self.item_size)
            self.file.flush()
            l = self.item_size
        self.map = mmap.mmap(self.file.fileno(), l)

        # TODO remove buffer in favour of just tscache
        self.buffer = []
        self.tscache = OrderedDict()

    def __len__(self):
        return self.file_len + len(self.buffer)


    def get_file(self, index):
        data = struct.unpack_from(self.format, self.map, index * self.item_size)
        return data[0], data[1:]


    def get(self, i):
        if i >= self.file_len:
            return self.buffer[i - self.file_len]
        else:
            return self.get_file(i)

    __getitem__ = get


    def flush(self, andfile=False):
        self.map.resize((self.file_len + len(self.buffer)) * self.item_size)
        for timestamp, data in self.buffer:
            struct.pack_into(self.format,
                self.map, (self.file_len * self.item_size),
                timestamp, *data)
            self.file_len += 1

        self.buffer = []
        if andfile:
            self.map.flush()


    def find_index(self, ts):
        '''
        Finds the index with timestamp <= ts
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

        while len(self.tscache) > 10 * len(self):
            self.tscache.popitem()

        return s


    def get_at(self, begin_ts, end_ts=None):
        s = self.find_index(begin_ts)
        if end_ts:
            e = self.find_index(end_ts) + 1
        else:
            s = len(self)

        return (self.get(i) for i in xrange(s, e))


    def append(self, timestamp, data):
        self.buffer.append((timestamp, data))
        if len(self.buffer) > 1024:
            self.flush()


    def close(self):
        self.flush(True)
        self.map.close()
        self.file.close()


    def __del__(self):
        self.close()


def test():
    import time
    import random

    start = now = time.time()

    s1 = TimeSeries('test1', 'B', '__test')
    for i in xrange(512):
        s1.append(start + i, (i % 256,))

    s1.flush()

    for i in xrange(512):
        print s1[i]

    print
    print list(s1.get_at(now + 10, now + 20))

    s2 = TimeSeries('test2', 'Bd', '__test')
    for i in xrange(10240):
        r = random.random()
        now += r / 100.
        s2.append(now, (i % 256, r))

    s2.flush()
    for i in xrange(128):
        r = random.random() * 1024
        print list(s2.get_at(start + r, start + r + 1.0))


if __name__ == '__main__':
    test()
