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

class TimeoutError(IOError):
    pass


class OBD2Frame(object):
    def __init__(self, frame):
        self.id     = frame.id;
        self.len    = frame.data[0]
        self.mode   = frame.data[1]
        self.pid    = frame.data[2]
        self.data   = frame.data[3:self.len+3-2]


class OBD2(object):
    def __init__(self, app, can):
        self.app = app
        self.can = can
        self.can.subscribe(self.read, ids=OBD2_IDS)

        self.read_waiters = defaultdict(set)
        self.read_timeouts = []

        self.supported_pids = []

        start = lambda:greenlet.greenlet(self.init).switch()
        ioloop.add_timeout(time.time() + 2, start)


    def query(self, mode, pid):
        frame = Frame()
        frame.id    = OBD2_REQUEST
        frame.len   = 8
        frame.flags = 0
        frame.data  = (2, mode, pid, 0x55, 0x55, 0x55, 0x55, 0x55)
        self.can.adapter.write(frame)


    def query_block(self, mode, pid):
        self.query(mode, pid)
        return self.read_block(mode | 0x40, pid)


    def read_block(self, mode, pid, timeout=0.5):
        current = greenlet.getcurrent()
        s = self.read_waiters[mode, pid]
        s.add(current)

        def timeout_cb():
            s.remove(current)
            current.throw(TimeoutError('Read timeout exceeded'))

        _t = ioloop.add_timeout(time.time() + timeout, timeout_cb)
        frame = current.parent.switch()

        ioloop.remove_timeout(_t)
        return frame


    def query_pid_block(self, mode, pid):
        frame = self.query_block(mode, pid)
        pid_type = PID.get(frame.pid)
        if pid_type:
            if pid_type.func:
                value = pid_type.func(*frame.data)
            else:
                value = frame.data
            log.info('PID %02X %s: %s' % (pid, pid_type.desc, value))
        else:
            log.info('PID %02X %s: %s' % (pid, 'Unknown', frame.data))


    def read(self, frame):
        obd2frame = OBD2Frame(frame)

        waiting = self.read_waiters[obd2frame.mode, obd2frame.pid]
        for i in waiting:
            i.switch(obd2frame)

        if not waiting:
            log.info(frame)


    def get_supported_pids(self):
        # TODO multiple ECUs could respond here.
        # make table for each
        supported = [0]
        for i in xrange(0, 0xFF, 0x20):
            if not supported[-1] == i:
                break

            frame = self.query_block(0x01, i)
            for j, byte in enumerate(frame.data):
                for k in xrange(8):
                    pid = i + j*8 + k + 1
                    sup = byte & (0x80>>k)
                    if sup:
                        supported.append(pid)

        return supported


    def get_vin(self):
        # request vehicle info (VIN)

        # supported_frame = self.query_block(0x09, 0x00)
        # if not frame.data[0] & 0x3:
        #     print 'VIN not supported'
        #     print map(hex, frame.data)

        num_frames = self.query_block(0x09, 0x01).data[0]

        self.query(0x09, 0x02)
        vin_frames = [self.read_block(0x09 & 0x40, 0x02) for i in xrange(num_frames)]

        print vin_frames
        vin_frames.sort(lambda x:x.data[0])
        vin = map(chr, [i.data[1:] for i in vin_frames])
        print vin

        return vin


    def init(self):
        log.info('OBD2 Init')

        # self.get_vin()
        # return

        self.supported_pids = self.get_supported_pids()
        print self.supported_pids

        log_msg = []
        for p in self.supported_pids:
            pid = PID.get(p)
            if pid:
                log_msg.append('%02x - %s' % (p, pid.desc))
            else:
                log_msg.append('%02x - %s' % (p, 'Unknown'))

        log.info('Vehicle supported PIDs: \n%s' %
            '\n'.join(log_msg))


        # query all PIDs
        for p in self.supported_pids:
            try:
                self.query_pid_block(0x01, p)
            except TimeoutError:
                print 'Error', p


        # vin = self.get_vin()
        # log.info('Vehicle VIN: %s' % vin)

        # - dump all DTC error codes / one time data
        # - start loop to request supported mode 0x01 values


    def start_log(self, interval):

        counters = {}
        for pid in self.supported_pids:
            p = PID[pid]
            name = 'obd.%02x' % pid
            counters[pid] = self.app.add_counter()


        def query():
            for pid in self.supported_pids:




        ioloop.PeriodicCallback(query, interval * 1000)

