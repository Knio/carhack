import re

class TimeSeriesInterface(object):
  _patterns = []
  class __metaclass__(type):
    def __init__(cls, name, bases, dict):
      type.__init__(cls, name, bases, dict)
      pattern = getattr(cls, 'name_pattern', None)
      if pattern:
        TimeSeriesInterface._patterns.append((pattern, cls))

  @staticmethod
  def get_handler(name):
    for pattern, cls in TimeSeriesInterface._patterns:
      if re.match(pattern, name):
        return cls
    raise Exception('no handler found for name %r' % name)

  def open(self, fname):
    raise NotImplementedError

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
    raise NotImplementedError


def test(logging_type, data_generator):
  import os
  import tempfile
  import cgitb
  cgitb.enable(format='text')
  fileno, fname = tempfile.mkstemp()
  print fname
  os.close(fileno)

  log = None

  def assert_eq(a, b):
    assert a == b, '%r should be %r' % (a, b)

  def assert_raises(a, b, *r, **kw):
    try:
      a(*r, **kw)
    except b:
      return
    assert False

  try:
    log = logging_type()
    log.open(fname)

    assert_raises(log.get, Exception, 0)
    assert_eq(log.get_range(0.0, 1.0), [])

    # [0, 1, 2, 3, 4, 5]
    data = [(float(i), data_generator.next()) for i in xrange(6)]


    def check():
      for i, d in enumerate(data):
        assert_eq(d, log[i])

      assert_eq(log.get_range(-0.5), data)
      assert_eq(log.get_range( 0.0), data)
      assert_eq(log.get_range( 0.5), data)
      assert_eq(log.get_range( 1.0), data[1:])
      assert_eq(log.get_range( 1.5), data[1:])
      assert_eq(log.get_range( 5.5), data[5:])

      assert_eq(log.get_range(-0.5, -0.5), [])
      assert_eq(log.get_range( 0.0,  0.0), [])
      assert_eq(log.get_range( 0.5,  5.0), data[0:5])
      assert_eq(log.get_range( 0.5,  0.5), data[0:1])
      assert_eq(log.get_range( 1.5,  2.5), data[1:3])
      assert_eq(log.get_range( 4.5,  5.5), data[4:6])

    for d in data:
      log.append(*d)

    check()

    log.close()
    log.close()

    assert os.path.getsize(fname) != 0

    log = logging_type()
    log.open(fname)

    check()

  finally:
    if log is not None:
      log.close()
    os.remove(fname)


  print 'Testing %s passed' % logging_type.__name__
