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


class Moo(TimeSeriesInterface):
    handles = 'moo'

print TimeSeriesInterface.get('moo')
