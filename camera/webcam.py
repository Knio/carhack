import time
import threading
from cStringIO import StringIO
import logging

log = logging.getLogger('webcam')

# TODO make this support multiple cameras
class Webcam(object):
    def __init__(self, app, interval=0.5, log_interval=0.5):
        self.app = app

        self.interval = interval
        self.log_interval = log_interval
        self.last_log = 0.0
        self.jpeg_data = None

        self.cam = None
        try:
            from VideoCapture import Device
            # NOTE: must initialize this from the main thread, it seems
            self.cam = Device()
        except:
            log.warn('webcam failed to initialize')

    def get_image(self):
        return self.jpeg_data

    def tick(self):
        file = StringIO()
        image = self.cam.getImage(1)
        image.save(file, 'jpeg')
        self.jpeg_data = file.getvalue()

        now = time.time()
        if self.log_interval and self.last_log+self.log_interval < now:
            self.last_log = now
            fname = 'logs/webcam/cam.%s.jpg' % \
                time.strftime('%Y-%m-%d.%H.%M.%S', now)
            open(fname, 'wb').write(self.jpeg_data)

        time.sleep(self.interval)

    def start(self):
        def loop():
            while 1:
                self.tick()
        thread = threading.Thread(target=loop)
        thread.start()
