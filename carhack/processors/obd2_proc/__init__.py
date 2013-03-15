import logging

from carhack.processors import Processor, subscribe
from carhack.lib import obd2

log = logging.getLogger('obd2_proc')

nice_names = {
  0x04: 'engine_load',
  0x05: 'coolant_temp',
  0x06: 'short_term_fuel_trim_bank1',
  0x07: 'long_term_fuel_trim_bank1',
  0x08: 'short_term_fuel_trim_bank2',
  0x09: 'long_term_fuel_trim_bank2',
  0x0a: 'fuel_rail_pressure',
  0x0b: 'intake_manifold_abs_pressure',
  0x0c: 'rpm',
  0x0d: 'vehicle_speed',
  0x0e: 'timing_advance',
  0x0f: 'intake_air_temp',
  0x10: 'MAF_rate',
  0x11: 'abs_throttle_position_a',

  0x14:('o2_sensor_voltage_bank1_sensor1',
        'short_term_fuel_trim_bank1_sensor1'),
  0x15:('o2_sensor_voltage_bank1_sensor2',
        'short_term_fuel_trim_bank1_sensor2'),
  0x16:('o2_sensor_voltage_bank1_sensor3',
        'short_term_fuel_trim_bank1_sensor3'),
  0x17:('o2_sensor_voltage_bank1_sensor4',
        'short_term_fuel_trim_bank1_sensor4'),
  0x18:('o2_sensor_voltage_bank2_sensor1',
        'short_term_fuel_trim_bank2_sensor1'),
  0x19:('o2_sensor_voltage_bank2_sensor2',
        'short_term_fuel_trim_bank2_sensor2'),
  0x1a:('o2_sensor_voltage_bank2_sensor3',
        'short_term_fuel_trim_bank2_sensor3'),
  0x1b:('o2_sensor_voltage_bank2_sensor4',
        'short_term_fuel_trim_bank2_sensor4'),
  0x1f: 'run_time_since_engine_start',

  0x21: 'distance_traveled_with_mil',
  0x22: 'fuel_rail_pressure_manifold_vacuum',
  0x23: 'fuel_rail_pressure',
  0x24:('wide_range_o2_eqivalance_ratio_bank1_sensor1',
        'wide_range_o2_sensor_voltage_bank1_sensor1'),
  0x25:('wide_range_o2_eqivalance_ratio_bank1_sensor2',
        'wide_range_o2_sensor_voltage_bank1_sensor2'),
  0x26:('wide_range_o2_eqivalance_ratio_bank1_sensor3',
        'wide_range_o2_sensor_voltage_bank1_sensor3'),
  0x27:('wide_range_o2_eqivalance_ratio_bank1_sensor4',
        'wide_range_o2_sensor_voltage_bank1_sensor4'),
  0x28:('wide_range_o2_eqivalance_ratio_bank2_sensor1',
        'wide_range_o2_sensor_voltage_bank2_sensor1'),
  0x29:('wide_range_o2_eqivalance_ratio_bank2_sensor2',
        'wide_range_o2_sensor_voltage_bank2_sensor2'),
  0x2a:('wide_range_o2_eqivalance_ratio_bank2_sensor3',
        'wide_range_o2_sensor_voltage_bank2_sensor3'),
  0x2b:('wide_range_o2_eqivalance_ratio_bank2_sensor4',
        'wide_range_o2_sensor_voltage_bank2_sensor4'),
  0x2c: 'command_egr',
  0x2d: 'egr_error',
  0x2e: 'commanded_evap_purge',
  0x2f: 'fuel_level',

  0x30: 'warmups_since_dtc_cleared',
  0x31: 'distance_traveled_since_dtc_cleared',
  0x32: 'evap_system_vapor_pressure',
  0x33: 'absolute_barometric_pressure',

  0x3c: 'catalyst_temp_bank1_sensor1',
  0x3d: 'catalyst_temp_bank2_sensor1',
  0x3e: 'catalyst_temp_bank1_sensor2',
  0x3f: 'catalyst_temp_bank2_sensor2',
  
  0x42: 'control_module_voltage',
  0x43: 'absolute_load_value',
  0x44: 'commanded_equivilance_ratio',
  0x45: 'relative_throttle_position',
  0x46: 'ambient_air_temp',
  0x47: 'abs_throttle_position_b',
  0x49: 'accellerator_pedal_position_d',

  0x4a: 'accellerator_pedal_position_e',

  0x4c: 'commanded_throttle',
  0x4d: 'time_engine_running_with_mil',
  0x4e: 'time_since_mil_cleared',

  0x55: 'short_term_secondary_o2_sensor_trim_bank1',
  0x56: 'term_term_secondary_o2_sensor_trim_bank1',
  0x59: 'abs_fuel_rail_pressure',
  0x66:('mass_air_flow_bank1',
        'mass_air_flow_bank2'),

}

class OBD2Processor(Processor):
  def __init__(self, pub):
    super(OBD2Processor, self).__init__(pub)
    self.pids = {}
    for can_id in obd2.OBD2_RESPONSE_IDS:
      pub.subscribe('canusb.can.%03x' % can_id, self.read)


  def read(self, ts, value):
    frame = obd2.PID.parse_can(value['id'], *value['data'])
    # print type(frame)
    # print 'Processing: ' + str(frame.pid)
    # print frame.name

    x = frame.value
    self.pids[frame.pid] = x

    nice_name = nice_names.get(frame.pid, None)
    if not nice_name:
      log.info('unknown name for %r' % frame)
      return

    if isinstance(nice_name, tuple):
      for k, v in zip(nice_name, x):
        self.publish('obd2.%s' % k, ts, v)
      return

    self.publish('obd2.%s' % nice_name, ts, x)


processor = OBD2Processor
