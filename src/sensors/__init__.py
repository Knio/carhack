def get_sensor(name):
  module = __import__(name, globals(), level=0)
  # root = __import__('sensors.%s' % name, globals(), level=0)
  # module = getattr(root, name)
  sensor = module.sensor
  sensor.name = name
  return sensor
