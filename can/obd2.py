import logging

from pids import *
from frame import Frame

log = logging.getLogger('obd2')

OBD2_REQUEST = 0x7DF
OBD2_IDS = [0x7E8, 0x7E9, 0x7EA, 0x7EB, 0x7EC, 0x7ED, 0x7EE, 0x7EF]


class OBD2(object):
    def __init__(self, can):
        self.can = can
        self.can.subscribe(self.read, ids=OBD2_IDS)

        # request all 'PID Supported' modes
        # request vehicle info (VIN)
        # dump all DTC error codes / one time data
        # start loop to request supported mode 0x01 values


    def query(self, mode, pid):
        frame = Frame()
        frame.id    = OBD2_REQUEST
        frame.len   = 8
        frame.flags = 0
        frame.data  = (2, mode, pid, 0x55, 0x55, 0x55, 0x55, 0x55)
        self.can.adapter.write(frame)


    def read(self, frame):
        log.info(str(frame))

        bytes, mode, pid = frame.data[0:3]
        data = frame.data[3:3+bytes]

        if mode == 0x41:
            pid_type = PID.get(pid)
            if pid_type:
                if pid_type.func:
                    value = pid_type.func(*data)
                else:
                    value = data
                log.info('PID %02X %s: %s' % (pid, pid_type.desc, value))

