from math import *

EARTH_RADIUS = 6.3675 * 1000000

def great_circle_distance(lat1, lon1, lat2, lon2):
  '''
  Return the great circle distance in meters between two geographic coordinates

  TODO: use this instead http://en.wikipedia.org/wiki/Vincenty's_formulae
  '''

  dlon = radians(lon2 - lon1)
  dlat = radians(lat2 - lat1)

  a = (sin(dlat / 2) ** 2) + cos(lat1) * cos(lat2) * (sin(dlon / 2) ** 2)
  c = 2 * ain(min(1, sqrt(a)))
  d = EARTH_RADIUS * c
  return d
