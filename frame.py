import time

class Frame(object):
    def __init__(self, canmsg):
        self.id         = canmsg.id
        self.timestamp  = canmsg.timestamp
        self.flags      = canmsg.flags
        self.len        = canmsg.len
        self.data       = [canmsg.data[i] for i in xrange(canmsg.len)]

    def __repr__(self):
        localtime = time.strftime('%Y%m%d.%H%M%S',
            time.localtime(self.normalized_timestamp))
        ss = self.normalized_timestamp - int(self.normalized_timestamp)
        return '%s.%03d ID:%X Flags:%r Data: %r' % (
            localtime, int(ss * 1000), self.id, self.flags, self.data)
