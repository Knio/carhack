import time
import struct

class Frame(object):
    '''
    Frame of CAN data
    '''
    format = '!dHBB8B'
    format_len = struct.calcsize(format)

    def __init__(self, canmsg=None):

        if isinstance(canmsg, basestring):
            x = struct.unpack(self.format, canmsg)
            (   self.timestamp,
                self.id,
                self.flags,
                self.len) = x[:4]
            self.data = x[4:4+self.len]

        elif canmsg is None:
            self.id         = 0
            self.timestamp  = 0
            self.flags      = 0
            self.len        = 0
            self.data       = ()

        else:
            self.id         = canmsg.id
            self.timestamp  = canmsg.timestamp
            self.flags      = canmsg.flags
            self.len        = canmsg.len
            self.data       = tuple(canmsg.data[i] for i in xrange(canmsg.len))

    def __repr__(self):
        localtime = time.strftime('%Y%m%d.%H%M%S',
            time.localtime(self.timestamp))
        ss = self.timestamp - int(self.timestamp)
        data = '(%s)' % ', '.join('%3d' % i for i in self.data)
        return '%s.%03d ID:%03X Flags:%r Data: %s' % (
            localtime, int(ss * 1000), self.id, self.flags, data)

    def tostring(self):
        data = self.data + ((0,)*(8-self.len))
        return struct.pack(self.format,
            self.timestamp, self.id, self.flags, self.len, *data)

    def tojson(self):
        import json
        return json.dumps(dict(
            timestamp=self.timestamp,
            id=self.id,
            flags=self.flags,
            len=self.len,
            data=self.data
        ))


if __name__ == '__main__':
    f = Frame()
    print f
    print Frame(f.tostring())
