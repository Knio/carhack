
from carhack.carapp import app


class Sensor(object):
  def publish(self, name, timestamp, value, skip_duplicates=False):
    if getattr(self, 'last_value', None) == value and skip_duplicates:
      return
    name = '%s.%s' % (self.name, name)
    app.live_trip.publish(name, timestamp, value)
    self.last_value = value

  def close(self):
    pass


def get_sensor(name):
  carapp = __import__('carhack.sensors.%s' % name, globals(), level=0)
  module = getattr(carapp.sensors, name)
  sensor = module.sensor
  sensor.name = name
  return sensor
