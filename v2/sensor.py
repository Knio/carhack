
from carapp import app

class Sensor(object):
  def publish(self, name, timestamp, value):
    name = '%s.%s' % (self.name, name)
    app.live_trip.publish(name, timestamp, value)
