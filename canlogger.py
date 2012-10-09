import time
import canlog
import pycanusb

class CANLogger(object):
    def __init__(self):
        fname = 'canlog.%s.log' % time.strftime('%Y-%m-%d.%H.%M.%S')
        self.log = canlog.CANLog('can.log')
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
    fname = sys.argv[1]
    logger = CANLogger()

    # logger.simulate(canlog.CANLog(fname))
    try:
        while 1:
            time.sleep(2)
            print logger.adapter.status()

    except KeyboardInterrupt:
        pass

    finally:
        logger.close()

