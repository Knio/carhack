import time
import logging

log = logging.getLogger('can')

from collections import defaultdict

import tornado.ioloop

ioloop = tornado.ioloop.IOLoop.instance()

class CAN(object):
    def __init__(self, simulate=False, logging=True):
        if not simulate:
            import pycanusb
            self.adapter = pycanusb.open(bitrate='500', callback=self.raw_read)
        self.listeners = defaultdict(set)
        self.subscriptions = {}
        self.last_frame = {}

        if logging:
            import canlog
            fname = 'logs/can/canlog.%s.log' \
                % time.strftime('%Y-%m-%d.%H.%M.%S')
            self.log = canlog.CANLog(fname)
            self.subscribe(self.log)

        ioloop.PeriodicCallback(self.status, 5000).start()


    def status(self):
        s = can.adapter.status()
        log.info(can.adapter.statusText(s))
        # TODO if status is bad, reconnect

    def simulate(self, frames):
        import threading

        if not frames:
            return

        def go():
            start_rt = time.time()
            start_st = frames[0].timestamp

            for frame in frames:
                s1 = frame.timestamp - start_st
                s2 = time.time() - start_rt
                s = s1 - s2
                if s > 0:
                    time.sleep(s)

                self.read(frame)

        thread = threading.Thread(target=go)
        thread.daemon = True
        thread.start()


    def raw_read(self, frame):
        '''
        The CANUSB callback function runs in it's own thread.
        Move the call to tornado's thread
        '''
        ioloop.add_callback(lambda:self.read(frame))


    def read(self, frame):
        id = frame.id
        last = self.last_frame.get(id)
        self.last_frame[id] = frame
        duplicate = last and last.data == frame.data
        for k in [id, None]:
            for callback, suppress_duplicates in self.listeners[k]:
                if duplicate and suppress_duplicates:
                    continue
                self.call_callback(callback, frame)

    # def interactive(self):
    #     import msvcrt
    #     while 1:
    #         c = getch()

    def subscribe(self, callback, ids=None, suppress_duplicates=False):
        if not ids:
            ids = [None]

        self.subscriptions[callback] = (ids, suppress_duplicates)

        for id in ids:
            self.listeners[id].add((callback, suppress_duplicates))

            if suppress_duplicates:
                last = self.last_frame.get(id)
                if last:
                    self.call_calback(callback, last)

    def unsubscribe(self, callback):
        ids, suppress_duplicates = self.subscriptions.pop(callback)
        for id in ids:
            self.listeners[id].remove((callback, suppress_duplicates))

    def call_callback(self, callback, *args, **kwargs):
        try:
            callback(*args, **kwargs)
        except:
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    can = CAN()

    try:
        while 1:
            time.sleep(2)
            s = can.adapter.status()
            print can.adapter.statusText(s)
            if s != 0:
                raise Exception

    except KeyboardInterrupt:
        print
        print 'Closing'
        print

    finally:
        can.log.close()

