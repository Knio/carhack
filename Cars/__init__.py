import logging

class IDMeta(type):
    def __init__(cls, name, bases, dict):
        for k, v in dict.items():
            if k == 'read':
                def _read(*args):
                    for b in bases:
                        b.read(*args)
                    return v(*args)
                dict[k] = _read
        super(IDMeta, cls).__init__(name, bases, dict)
        cls.id = name[2:]

class ID(object):
    def __init__(self):
        pass

    def read(self, frame):
        self.last_frame = frame

    def log(self, msg, *args):
        log = logging.getlogger('nissan')
        log.info('%r %s' % (self.last_frame, msg), *args)
