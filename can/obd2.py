import time
import logging
import greenlet
import weakref
import tornado.ioloop
from collections import defaultdict

from pids import *
from frame import Frame

log = logging.getLogger('obd2')

OBD2_REQUEST = 0x7DF
OBD2_IDS = [0x7E8, 0x7E9, 0x7EA, 0x7EB, 0x7EC, 0x7ED, 0x7EE, 0x7EF]

ioloop = tornado.ioloop.IOLoop.instance()


class OBD2Frame(object):
    def __init__(self, frame):
        self.id     = frame.id;
        self.len    = frame.data[0]
        self.mode   = frame.data[1]
        self.pid    = frame.data[2]
        self.data   = frame.data[3:self.len]

class OBD2(object):
    def __init__(self, can):
        self.can = can
        self.can.subscribe(self.read, ids=OBD2_IDS)

        self.read_waiters = defaultdict(set)
        self.read_timeouts = []

        self.supported_pids = []

        greenlet.greenlet(self.init).switch()


    def query(self, mode, pid):
        frame = Frame()
        frame.id    = OBD2_REQUEST
        frame.len   = 8
        frame.flags = 0
        frame.data  = (2, mode, pid, 0x55, 0x55, 0x55, 0x55, 0x55)
        self.can.adapter.write(frame)


    def query_block(self, mode, pid):
        self.query(mode, pid)
        return self.read_block(mode, pid)


    def read_block(self, mode, pid, timeout=1.0):
        current = greenlet.getcurrent()
        s = self.read_waiters[mode, pid]
        s.add(current)

        def timeout_cb():
            s.remove(current)
            current.throw(IOError)

        _t = ioloop.add_timeout(now() + timeout, timeout_cb)
        frame = current.parent.switch()

        ioloop.remove_timeout(_t)
        return frame


    def init(self):
        # - request all 'PID Supported' modes
        # - dump all DTC error codes / one time data
        # - start loop to request supported mode 0x01 values

        pid_mask = [0] * 0xE0
        for i in xrange(0, 0xE0, 0x20):
            frame = self.query_block(0x01, i)
            for j in frame.data:
                for k in xrange(8):
                    pid_mask[i + k] = j & 1
                    j <<= 1

        self.supported_pids = [i for i,s in enumerate(pid_mask) if s]

        log = []
        for p in pids:
            pid = PID[p]
            log.append('%02x - %s' % (p, pid.desc))

        log.info('Vehicle supported PIDs: \n%s' %
            '\n'.join(log))

        # - request vehicle info (VIN)

    def timeout(self):
        now = time.time()
        i = 0;
        for i, (t, g, s) in self.read_timeouts:
            if t < now:
                s.remove(g)
            else:
                break
        self.read_timeouts[0:i] = []


    def read(self, frame):
        log.info(str(frame))

        obd2frame = OBD2Frame(frame)

        # mode 0x01 response
        if obd2frame.mode == 0x41:
            pid_type = PID.get(obd2frame.pid)
            if pid_type:
                if pid_type.func:
                    value = pid_type.func(*obd2frame.data)
                else:
                    value = data
                log.info('PID %02X %s: %s' % (pid, pid_type.desc, value))

        waiting = self.read_waiters[mode, pid]
        for i in waiting:
            i.switch(frame)

