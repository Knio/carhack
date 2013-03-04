import inspect
import logging

from carhack import app
from carhack.processors import Processor, subscribe

log = logging.getLogger('test_proc')

def unsigned_short(a, b):
  return (a<<8) | b

def signed_short(a, b):
  x = (a << 8) | b
  if (x & 0x8000):
    x -= 0x10000
  return x

def percent(a):
  return 100 * (a / 255.)

def bit(x):
  return int(x != 0)


def wrap(func):
  def f(ts, value):
    return func(ts, *value['data'])
  return f


class Nissan370ZProcessor(Processor):
  def __init__(self, pub):
    super(Nissan370ZProcessor, self).__init__(pub)
    for name, method in inspect.getmembers(self):
      if not name.startswith('can_'):
        continue
      pub.subscribe(
        'canusb.can.%s' % name.split('_')[1],
        wrap(method))

  def can_002(self, ts, A, B, C, D, E):
    steering_position = signed_short(B, A)
    self.publish('steering_position', ts, steering_position)

  def can_180(self, ts, A, B, C, D, E, F, G, H):
    rpm = signed_short(B, A)
    throtle_position = percent(F)
    self.publish('rpm_a', ts, rpm)
    self.publish('throtle_position', ts, throtle_position)

  def can_1f9(self, ts, A, B, C, D, E, F, G, H):
    rpm = signed_short(D, C)
    self.publish('rpm_b', ts, rpm)

  def can_215(self, ts, A, B, C, D, E, F):
    ac_indicator = bit(B & 0x08)
    self.publish('ac_indicator', ts, ac_indicator)

  def can_216(self, ts, A, B):
    clutch_pedal_to_floor = bit(A & 0x08)
    self.publish('clutch_pedal_to_floor_a', ts, clutch_pedal_to_floor)

  def can_280(self, ts, A, B, C, D, E, F, G, H):
    vehicle_speed = unsigned_short(F, E)
    self.publish('vehicle_speed_a', ts, vehicle_speed)

  def can_351(self, ts, A, B, C, D, E, F, G, H):
    clutch_pedal_to_floor = bit(H & 0x04)
    self.publish('clutch_pedal_to_floor_a', ts, clutch_pedal_to_floor)

  def can_354(self, ts, A, B, C, D, E, F, G, H):
    tcs_indicator = bit(~E & 0x40)
    brake_light   = bit( G & 0x10)
    self.publish('tcs_indicator', ts, tcs_indicator)
    self.publish('brake_light', ts, brake_light)

  def can_35d(self, ts, A, B, C, D, E, F, G, H):
    wiper_status = {
      0: 0,
      64: 1,
      192: 2,
      224: 3,
    }.get(C, 255)
    car_moving  = bit(E == 0x40)
    car_stopped = bit(E == 0x08)
    self.publish('wiper_status', ts, wiper_status)
    self.publish('car_moving', ts, car_moving)
    self.publish('car_stopped', ts, car_stopped)

  def can_421(self, ts, A, B):
    gear = {
      24: 0,
      128: 1,
      136: 2,
      144: 3,
      152: 4,
      160: 5,
      168: 6,
      16: -1,
    }.get(A, 255)
    self.publish('6mt', ts, gear)

  def can_551(self, ts, A, B, C, D, E, F, G, H):
    sensor = A
    engine_revolutions = B

    crusie_control_master_a = bit(E & 0x01)
    crusie_control_master_b = bit(F & 0x50)

    self.publish('unknown_sensor_551_a', ts, sensor)
    self.publish('engine_revolutions', ts, engine_revolutions)
    self.publish('crusie_control_master_a', ts, crusie_control_master_a)
    self.publish('crusie_control_master_b', ts, crusie_control_master_b)

  def can_580(self, ts, A, B, C, D, E):
    rpm = unsigned_short(A, B)
    self.publish('rpm_c', ts, rpm)

  def can_5c5(self, ts, A, B, C, D, E, F, G, H):
    parking_brake_indicator = bit(A & 0x04)
    self.publish('parking_brake_indicator', ts, parking_brake_indicator)

  def can_60d(self, ts, A, B, C, D, E, F, G, H):
    headlights            = bit(A & 0x02)
    running_lights        = bit(A & 0x04)
    driver_door_open      = bit(A & 0x10)
    passenger_door_open   = bit(A & 0x20)

    left_turn_signal  = bit(B & 0x20)
    right_turn_signal = bit(B & 0x40)

    driver_door_locked  = bit(C & 0x08)
    car_locked          = bit(C & 0x10)

    self.publish('headlights', ts, headlights)
    self.publish('running_lights', ts, running_lights)
    self.publish('driver_door_open', ts, driver_door_open)
    self.publish('passenger_door_open', ts, passenger_door_open)
    self.publish('left_turn_signal', ts, left_turn_signal)
    self.publish('right_turn_signal', ts, right_turn_signal)
    self.publish('driver_door_locked', ts, driver_door_locked)
    self.publish('car_locked', ts, car_locked)



processor = Nissan370ZProcessor
