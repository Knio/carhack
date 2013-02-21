def get_sensor(name):
  root = __import__('sensors.%s' % name, globals(), level=0)
  module = getattr(root, name)
  sensor = module.sensor
  sensor.name = name
  return sensor
