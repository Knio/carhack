

class ProcessorMeta(type):
  def __init__(cls, name, bases, dict):
    super(ProcessorMeta, cls).__init__(name, bases, dict)
    subscribe_list = []
    for func_name, val in dict.iteritems():
      series = getattr(val, '_subscribe_series', None)
      if series is None:
        continue
      subscribe_list.append((series, func_name))

    cls._subscribe_list = subscribe_list


class Processor(object):
  __metaclass__ = ProcessorMeta

  def __init__(self, publisher):
    self.publisher = publisher
    self._last_value = {}

    for series, func_name in type(self)._subscribe_list:
      method = getattr(self, func_name)
      publisher.subscribe(series, method)

  def publish(self, name, timestamp, value, compress=True):
    if compress and self._last_value.get(name, None) == value:
      return
    self._last_value[name] = value
    name = '%s.%s' % (self.name, name)
    self.publisher.publish(name, timestamp, value)


def subscribe(series):
  def decorator(func):
    func._subscribe_series = series
    return func

  return decorator


def get_processor(name):
  carapp = __import__('carhack.processors.%s' % name, globals(), level=0)
  module = getattr(carapp.processors, name)
  processor = module.processor
  processor.name = name
  return processor
