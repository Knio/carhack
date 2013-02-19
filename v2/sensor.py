
from carapp import app

class Sensor(object):
    def publish(self, name, timestamp, value):
        app.live_trip.publish(name, timestamp, value)
