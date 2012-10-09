import time
import canlog
import pycanusb

class CANLogger(object):
    def __init__(self):
        fname = 'canlog.%s.log' % time.strftime('%Y-%m-%d.%H.%M.%S')
        self.log = canlog.CANLog(fname)
        self.adapter = pycanusb.open(bitrate='500', callback=self.read)

    def simulate(self, frames):
        for frame in frames:
            self.read(frame)

    def read(self, frame):
        self.log.append(frame)
        print frame

    def close(self):
        self.log.close()


if __name__ == '__main__':
    logger = CANLogger()

    # import sys
    # fname = sys.argv[1]
    # logger.simulate(canlog.CANLog(fname))
    try:
        while 1:
            time.sleep(2)
            s = logger.adapter.status()
            print logger.adapter.statusText(s)
            if s != 0:
                raise Exception

    except KeyboardInterrupt:
        print 'Closing'
        print

    finally:
        logger.close()

