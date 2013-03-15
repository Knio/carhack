__all__ = ['OBD2_REQUEST_ID', 'OBD2_RESPONSE_IDS', 'PID', 'obd2_can_request']

import struct

signed = \
    lambda A: struct.unpack('@b', struct.pack('@B', A))[0]


OBD2_REQUEST_ID = 0x7DF
OBD2_RESPONSE_IDS = [
    0x7E8, 0x7E9, 0x7EA, 0x7EB,
    0x7EC, 0x7ED, 0x7EE, 0x7EF,
]

class obd2_can_request(object):
    def __init__(self, mode, pid):
        self.can_id = OBD2_REQUEST_ID
        self.mode = mode
        self.pid = pid
        self.bytes = [2, mode, pid, 0x55, 0x55, 0x55, 0x55, 0x55]

class PID(object):
    class __metaclass__(type):
        def __init__(cls, name, bases, dict):
            type.__init__(cls, name, bases, dict)
            if bases == (object,):
                return
            cls.desc = cls.__doc__ or ''
            cls.pid = int(name[1:], 16)
            PID._pids[cls.pid] = cls
            setattr(PID, name, cls)

    _pids = {}

    @staticmethod
    def parse_can(sender, *bytes):
        can_id      = sender
        if can_id not in OBD2_RESPONSE_IDS:
            raise ValueError('not an obd2 frame')
        num_bytes   = bytes[0]
        mode        = bytes[1]
        pid         = bytes[2]

        cls = PID._pids.get(pid, None)
        if not cls:
            raise ValueError('Unknown PID %X' % pid)

        obj = cls(mode, *bytes[3:num_bytes+1])
        return obj

    def __init__(self, mode, *bytes):
        self.mode = mode
        self.bytes = bytes

    def __getattr__(self, name):
        try:
            i = tuple('abcde').index(name)
            return self.bytes[i]
        except ValueError:
            raise AttributeError

    def __repr__(self):
        return '<PID %02X [%s] %s>' % (self.pid, self.name, self.value)

    @property
    def value(self):
        return self.bytes

def prop(func):
    @property
    def f(self):
        return func(*self.bytes)
    return f

@property
def supported(self):
    bits = (self.a << 24) | (self.b << 16) | (self.c << 8) | self.d
    return [self.pid + i for i in xrange(1, 33) if (bits << i) & (1<<32)]

@property
def dtc(self):
    return '%c%2X%2X' % (
        'PCBU'[self.a & 0xC0],
        self.a & ~0xC0,
        self.b)

def byte(a):
    return a

def percent(a):
    return 100 * (a / 255.)

def signed_percent(a):
    return 100 * ((a - 128) / 128.)

def short(a, b):
    return (a << 8) | b


class x00(PID):
    name = 'PIDs supported [01 - 20]'
    value = supported

class x20(PID):
    name = 'PIDs supported [21 - 40]'
    value = supported

class x40(PID):
    name = 'PIDs supported [41 - 60]'
    value = supported

class x60(PID):
    name = 'PIDs supported [61 - 80]'
    value = supported

class x80(PID):
    name = 'PIDs supported [81 - A0]'
    value = supported

class xA0(PID):
    name = 'PIDs supported [A1 - C0]'
    value = supported

class xC0(PID):
    name = 'PIDs supported [C1 - E0]'
    value = supported


class x01(PID):
    name = 'Monitor Status'
    # TODO

class x02(PID):
    name = 'DTC that caused required freeze frame data storage'
    value = dtc

class x03(PID):
    name = 'Fuel system status'
    # TODO

class x04(PID):
    '''
    LOAD_PCT = [current airflow] / [(peak airflow at WOT@STP as a function of rpm) * (BARO/29.92) * SQRT(298/(AAT+273))]
    Where:
    - STP = Standard Temperature and Pressure = 25 C, 29.92 in Hg BARO, SQRT = square root,
    - WOT = wide open throttle, AAT = Ambient Air Temperature and is in C

    Characteristics of LOAD_PCT are:
    - Reaches 100% at WOT at any altitude, temperature or rpm for both naturally aspirated and boosted engines.
    - Indicates percent of peak available torque.
    - Linearly correlated with engine vacuum
    - Often used to schedule power enrichment.
    - Compression ignition engines (diesels) shall support this PID using fuel flow in place of airflow for the above calculations.

    NOTE Both spark ignition and compression ignition engines shall support PID $04. See PID $43 for an additional definition
    of engine LOAD
    '''
    name = 'Calculated engine load value (%)'
    value = prop(percent)

class x05(PID):
    name = 'Engine coolant temperature (C)'
    value = prop(lambda a: a-40.)

# TODO Also bank 3 if two bytes returned
class x06(PID):
    name = 'Short term fuel trim - Bank 1 (%)'
    value = prop(signed_percent)

# TODO Also bank 3 if two bytes returned
class x07(PID):
    name = 'Long term fuel trim - Bank 1 (%)'
    value = prop(signed_percent)

# TODO Also bank 4 if two bytes returned
class x08(PID):
    name = 'Short term fuel trim - Bank 2 (%)'

# TODO Also bank 4 if two bytes returned
class x09(PID):
    name = 'Long term fuel trim - Bank 2 (%)'
    value = prop(signed_percent)

class x0A(PID):
    name = 'Fuel rail pressure (kPa g)'
    value = prop(lambda A: (A*3))

class x0B(PID):
    name = 'Intake manifold absolute pressure (kPa)'
    value = prop(byte)

class x0C(PID):
    name = 'Engine RPM'
    value = prop(lambda a,b: short(a,b)/4.)

class x0D(PID):
    name = 'Vehicle speed (km/h)'
    value = prop(byte)

class x0E(PID):
    name = 'Timing advance (degrees relative to #1 cylinder)'
    value = prop(lambda A: (A/2. - 64))

class x0F(PID):
    name = 'Intake air temperature (C)'
    value = prop(lambda A: (A-40.))

class x10(PID):
    name = 'MAF mass air flow rate (g/sec)'
    value = prop(lambda A,B: short(A, B) / 100.)

class x11(PID):
    name = 'Absolute throttle position (%)'
    value = prop(percent)

class x12(PID):
    '''
    One bit only set
    A0 - upstream of first catalytic converter
    A1 - downstream of first catalytic converter inlet
    A2 - atmosphere / off
    '''
    name = 'Commanded secondary air status'
    # TODO

class x13(PID):
    '''
    A0 - Bank 1 - Sensor 1 present at that location (O2S11)
    A1 - Bank 1 - Sensor 2 present at that location (O2S12)
    A2 - Bank 1 - Sensor 3 present at that location (O2S13)
    A3 - Bank 1 - Sensor 4 present at that location (O2S14)
    A4 - Bank 2 - Sensor 1 present at that location (O2S21)
    A5 - Bank 2 - Sensor 2 present at that location (O2S22)
    A6 - Bank 2 - Sensor 3 present at that location (O2S23)
    A7 - Bank 2 - Sensor 4 present at that location (O2S24)
    '''
    name = 'Location of oxygen sensors'
    # TODO

    # NOTE:
    # The following PIDs assume that PID 0x13 (above) is supported.
    # If PID 0x1D is supported instead, they have different meanings. :(

def o2_voltage_and_stft(a, b):
    return a/200., signed_percent(b)

class x14(PID):
    name = 'Oxygen sensor voltage, Short term fuel trim - Bank 1, Sensor 1'
    value = prop(o2_voltage_and_stft)

class x15(PID):
    name = 'Oxygen sensor voltage, Short term fuel trim - Bank 1, Sensor 2'
    value = prop(o2_voltage_and_stft)

class x16(PID):
    name = 'Oxygen sensor voltage, Short term fuel trim - Bank 1, Sensor 3'
    value = prop(o2_voltage_and_stft)

class x17(PID):
    name = 'Oxygen sensor voltage, Short term fuel trim - Bank 1, Sensor 4'
    value = prop(o2_voltage_and_stft)

class x18(PID):
    name = 'Oxygen sensor voltage, Short term fuel trim - Bank 2, Sensor 1'
    value = prop(o2_voltage_and_stft)

class x19(PID):
    name = 'Oxygen sensor voltage, Short term fuel trim - Bank 2, Sensor 2'
    value = prop(o2_voltage_and_stft)

class x1A(PID):
    name = 'Oxygen sensor voltage, Short term fuel trim - Bank 2, Sensor 3'
    value = prop(o2_voltage_and_stft)

class x1B(PID):
    name = 'Oxygen sensor voltage, Short term fuel trim - Bank 2, Sensor 4'
    value = prop(o2_voltage_and_stft)


class x1C(PID):
    '''
    01 - OBD II (California ARB)
    02 - OBD (Federal EPA)
    03 - OBD and OBD II
    04 - OBD I
    05 - Not OBD compliant
    06 - EOBD
    07 - EOBD and OBD II
    08 - EOBD and OBD
    09 - EOBD, OBD and OBD II
    0A - JOBD
    0B - JOBD and OBD II
    0C - JOBD and EOBD
    0D - JOBD, EOBD, and OBD II
    '''
    name = 'OBD requirements to which vehicle is designed'
    # TODO

class x1D(PID):
    name = 'Location of oxygen sensors'
    # TODO
    # NOTE - Changes the meaning of PIDs 0x14 - 0x1B above

class x1E(PID):
    name = 'Auxiliary input status'
    # TODO
    # A1 - Power Take Off (PTO) Status

class x1F(PID):
    name = 'Run time since engine start (seconds)'
    value = prop(short)

class x21(PID):
    name = 'Distance traveled with malfunction indicator lamp (MIL) on (km)'
    value = prop(short)

class x22(PID):
    name = 'Fuel rail pressure (relative to manifold vacuum) (kPa)'
    value = prop(lambda A,B: short(A, B) * 0.079)

class x23(PID):
    name = 'Fuel rail pressure (kPa g)'
    value = prop(lambda A,B: short(A,B) * 10)


def o2_eq_ratio_and_voltage(a, b, c, d):
    return short(a, b) / 32768., 4 * short(c, d) / 32768.

# The following PIDs assume that PID 0x13 (above) is supported.
# If PID 0x1D is supported instead, they have different meanings. :()
class x24(PID):
    name = 'Wide range oxygen sensor equivalence ratio (lambda), voltage (V) - Bank 1, Sensor 1'
    value = prop(o2_eq_ratio_and_voltage)

class x25(PID):
    name = 'Wide range oxygen sensor equivalence ratio (lambda), voltage (V) - Bank 1, Sensor 2'
    value = prop(o2_eq_ratio_and_voltage)

class x26(PID):
    name = 'Wide range oxygen sensor equivalence ratio (lambda), voltage (V) - Bank 1, Sensor 3'
    value = prop(o2_eq_ratio_and_voltage)

class x27(PID):
    name = 'Wide range oxygen sensor equivalence ratio (lambda), voltage (V) - Bank 1, Sensor 4'
    value = prop(signed_percent)

class x2E(PID):
    '''
    Commanded evaporative purge control valve displayed as a percent.
    EVAP_PCT shall be normalized to the maximum EVAP purge commanded output
    control parameter. If an on/off solenoid is used, EVAP_PCT shall
    display 0 % when purge is commanded off, 100 % when purge is commanded on.
    If a vacuum solenoid is duty-cycled, the EVAP purge valve duty cycle
    from 0 to 100 % shall be displayed. If a linear or stepper motor valve is
    used, the fully closed position shall be displayed as 0 %, and the fully
    open position shall be displayed as 100 %. Intermediate positions shall be
    displayed as a percent of the full-open position. For example, a
    stepper-motor EVAP purge valve that moves from 0 to 128 counts shall
    display 0 % at 0 counts, 100 % at 128 counts and 50 % at 64 counts.
    Any other actuation method shall be normalized to display 0 % when no purge
    is commanded and 100 % at the maximum commanded purge position/flow.
    '''
    name = 'Commanded evaporative purge (%)'
    value = prop(percent)

class x28(PID):
    name = 'Wide range oxygen sensor equivalence ratio (lambda), voltage (V) - Bank 2, Sensor 1'
    value = prop(o2_eq_ratio_and_voltage)

class x29(PID):
    name = 'Wide range oxygen sensor equivalence ratio (lambda), voltage (V) - Bank 2, Sensor 2'
    value = prop(o2_eq_ratio_and_voltage)

class x2A(PID):
    name = 'Wide range oxygen sensor equivalence ratio (lambda), voltage (V) - Bank 2, Sensor 3'
    value = prop(o2_eq_ratio_and_voltage)

class x2B(PID):
    name = 'Wide range oxygen sensor equivalence ratio (lambda), voltage (V) - Bank 2, Sensor 4'
    value = prop(o2_eq_ratio_and_voltage)

class x2C(PID):
    name = 'Commanded EGR (%)'
    value = prop(percent)

class x2D(PID):
    name = 'EGR Error (%)'
    value = prop(percent)

class x2F(PID):
    name = 'Fuel level input (%)'
    value = prop(percent)

class x30(PID):
    '''
    A warm-up is defined in the OBD regulations to be sufficient vehicle
    operation such that coolant temperature rises by at
    least 22 C (40 F) from engine starting and reaches
    a minimum temperature of 70 C (160 F) (60 C (140 F) for diesels)
    '''
    name = 'Number of warm-ups since diagnostic trouble codes cleared'
    value = prop(byte)

class x31(PID):
    name = 'Distance traveled since codes cleared (km)'
    value = prop(short)

class x32(PID):
    name = 'Evap system vapor pressure (Pa)'
    value = prop(lambda A,B: (struct.unpack('@h', struct.pack('@BB', A, B))[0]/4.))

class x33(PID):
    name = 'Absolute barometric pressure (kPa)'
    value = prop(byte)


def o2_eq_ratio_and_current(a, b, c, d):
    return short(a,b) / 32768., short(c, d) / 256. - 128.

class x34(PID):
    name = 'Wide range oxygen sensor equivalence ratio (lambda), current (mA) - Bank 1, Sensor 1'
    value = prop(o2_eq_ratio_and_current)

class x35(PID):
    name = 'Wide range oxygen sensor equivalence ratio (lambda), current (mA) - Bank 1, Sensor 2'
    value = prop(o2_eq_ratio_and_current)

class x36(PID):
    name = 'Wide range oxygen sensor equivalence ratio (lambda), current (mA) - Bank 1, Sensor 3'
    value = prop(o2_eq_ratio_and_current)

class x37(PID):
    name = 'Wide range oxygen sensor equivalence ratio (lambda), current (mA) - Bank 1, Sensor 4'
    value = prop(o2_eq_ratio_and_current)

class x38(PID):
    name = 'Wide range oxygen sensor equivalence ratio (lambda), current (mA) - Bank 2, Sensor 1'
    value = prop(o2_eq_ratio_and_current)

class x39(PID):
    name = 'Wide range oxygen sensor equivalence ratio (lambda), current (mA) - Bank 2, Sensor 2'
    value = prop(o2_eq_ratio_and_current)

class x3A(PID):
    name = 'Wide range oxygen sensor equivalence ratio (lambda), current (mA) - Bank 2, Sensor 3'
    value = prop(o2_eq_ratio_and_current)

class x3B(PID):
    name = 'Wide range oxygen sensor equivalence ratio (lambda), current (mA) - Bank 2, Sensor 4'
    value = prop(o2_eq_ratio_and_current)

class x3C(PID):
    name = 'Catalyst temperature - Bank 1, Sensor 1 (C)'
    value = prop(lambda A,B: short(A, B)/10. - 40)

class x3D(PID):
    name = 'Catalyst temperature - Bank 2, Sensor 1 (C)'
    value = prop(lambda A,B: short(A, B)/10. - 40)

class x3E(PID):
    name = 'Catalyst temperature - Bank 1, Sensor 2 (C)'
    value = prop(lambda A,B: short(A, B)/10. - 40)

class x3F(PID):
    name = 'Catalyst temperature - Bank 2, Sensor 2 (C)'
    value = prop(lambda A,B: short(A, B)/10. - 40)


###############################################################################

class x41(PID):
    '''
    The bit in this PID shall report two pieces of information for each monitor:

    1)    Monitor enable status for the current driving cycle. This bit shall indicate when a monitor is disabled in a manner such that there is
          no way for the driver to operate the vehicle for the remainder of the driving cycle and make the monitor run. Typical examples are:
              - Engine-off soak not long enough (e.g., cold start temperature conditions not satisfied),
              - Monitor maximum time limit or number of attempts/aborts exceeded,
              - Ambient air temperature too low or too high,
              - BARO too low (high altitude).
          The monitor shall not indicate "disabled" for operator-controlled conditions such as rpm, load, throttle position, minimum time limit
          not exceeded, ECT, TP, etc.

    2)    Monitor completion status for the current driving/monitoring cycle. Status shall be reset to "not complete" upon starting a new
          monitoring cycle. Note that some monitoring cycles can include various engine-operating conditions; other monitoring cycles begin
          after the ignition key is turned off. Some status bits on a given vehicle can utilise engine-running monitoring cycles while others can
          utilise engine-off monitoring cycles. Resetting the bits to "not complete" upon starting the engine will accommodate most engine-running and engine-off monitoring cycles, however, manufacturers are free to define their own monitoring cycles.

          NOTE PID $41 bits shall be utilised for all non-continuous monitors which are supported, and change completion status in PID $01.
          If a non-continuous monitor is not supported or always shows "complete", the corresponding PID $41 bits shall indicate disabled
          and complete. PID $41 bits may be utilised at the vehicle manufacturer's discretion for all continuous monitors which are supported
          with the exception of bit 03 which shall always show CCM (Comprehensive Component Monitoring) as enabled for spark ignition
          and compression ignition engines

      A - Reserverd (0)

      B0 - Misfire monitoring enabled
      B1 - Fuel system monitoring enabled
      B2 - Comprehensive component monitoring enabled
      B3 - Reserverd (0)

      B4 - Misfire monitoring complete
      B5 - Fuel system monitoring complete
      B6 - Comprehensive component monitoring complete
      B7 - Reserverd (0)

      C0 - Catalyst monitoring enabled
      C1 - Heated catalyst monitoring enabled
      C2 - Evaporative system monitoring enabled
      C3 - Secondary air system monitoring enabled
      C4 - A/C system refrigerant monitoring enabled
      C5 - Oxygen sensor monitoring enabled
      C6 - Oxygen sensor heater monitoring enabled
      C7 - EGR system monitoring enabled

      D0 - Catalyst monitoring complete
      D1 - Heated catalyst monitoring complete
      D2 - Evaporative system monitoring complete
      D3 - Secondary air system monitoring complete
      D4 - A/C system refrigerant monitoring complete
      D5 - Oxygen sensor monitoring complete
      D6 - Oxygen sensor heater monitoring complete
      D7 - EGR system monitoring complete
    '''
    name = 'Monitor status this drive cycle'
    # TODO

class x42(PID):
    name = 'Control module voltage (V)'
    value = prop(lambda A,B: short(A, B)/1000.)

class x43(PID):
    '''
    The absolute load value has some different characteristics than the LOAD_PCT defined in PID 04 This definition, although restrictive,
    will standardise the calculation. LOAD_ABS is the normalised value of air mass per intake stroke displayed as a percent.

    LOAD_ABS = [air mass (g / intake stroke)] / [1.184 (g / intake stroke) * cylinder displacement in litres]

    Derivation:
    - air mass (g / intake stroke) = [total engine air mass (g/sec)] / [rpm (revs/min)* (1 min / 60 sec) * (1/2 # of cylinders (strokes / rev)],
    - LOAD_ABS = [air mass (g)/intake stroke] / [maximum air mass (g)/intake stroke at WOT@STP at 100% volumetric efficiency] * 100%.

    Where:
    - STP = Standard Temperature and Pressure = 25 C, 29.92 in Hg (101.3 kPa) BARO, WOT = wide open throttle.

    The quantity (maximum air mass (g)/intake stroke at WOT@STP at 100% volumetric efficiency) is a constant for a given cylinder sw ept
    volume. The constant is 1.184 (g/litre 3) * cylinder displacement (litre 3/intake stroke) based on air density
    at STP.

    Characteristics of LOAD_ABS are:
    - Ranges from 0 to approximately 0.95 for naturally aspirated engines, 0 - 4 for boosted engines,
    - Linearly correlated with engine indicated and brake torque,
    - Often used to schedule spark and EGR rates,
    - Peak value of LOAD_ABS correlates with volumetric efficiency at WOT.,
    - Indicates the pumping efficiency of the engine for diagnostic purposes.

    Spark ignition engine are required to support PID $43. Compression ignition (diesel) engines are not required to support this PID.
    NOTE  See PID $04 for an additional definition of engine LOAD.
    '''
    name = 'Absolute load value (%)'
    value = prop(lambda A,B: short(A, B)*100/255.)


class x44(PID):
    '''
    Fuel systems that utilise conventional oxygen sensor shall display the commanded open loop equivalence ratio while the fuel control
    system is in open loop. EQ_RAT shall indicate 1.0 while in closed loop fuel.

    Fuel systems that utilise wide-range/linear oxygen sensors shall display the commanded equivalence ratio in both open loop and
    closed loop operation.

    To obtain the actual A/F ratio being commanded, multiply the stoichiometric A/F ratio by the equivalence ratio. For example, for
    gasoline, stoichiometric is 14.64:1 ratio. If the fuel control system was commanding an 0.95 EQ_RAT, the commanded A/F ratio to the
    engine would be 14.64 * 0.95 = 13.9 A/F

      < 1.0 - Rich
      > 1.0 - Lean
    '''
    name = 'Commanded equivalence ratio'
    value = prop(lambda A,B: short(A, B)/32768.)

class x45(PID):
    name = 'Relative throttle position'
    value = prop(percent)

class x46(PID):
    name = 'Ambient air temperature'
    value = prop(lambda A: (A-40.))

class x47(PID):
    name = 'Absolute throttle position B (%)'
    value = prop(percent)

class x48(PID):
    name = 'Absolute throttle position C (%)'
    value = prop(percent)

class x49(PID):
    name = 'Accelerator pedal position D (%)'
    value = prop(percent)

class x4A(PID):
    name = 'Accelerator pedal position E (%)'
    value = prop(percent)

class x4B(PID):
    name = 'Accelerator pedal position F (%)'
    value = prop(percent)

class x4C(PID):
    name = 'Commanded throttle actuator (%)'
    value = prop(percent)

class x4D(PID):
    name = 'Time run by the engine while MIL activated (minutes)'
    value = prop(short)

class x4E(PID):
    name = 'Time since diagnostic trouble codes cleared (minutes)'
    value = prop(short)

    ####################################
    # 0x4F - 0xFF Reserved by J1979-2002

class x4F(PID):
    name = 'Maximum value for equivalence ratio, oxygen sensor voltage, oxygen sensor current, and intake manifold absolute pressure (lambda, V, mA, kPa)'
    value = prop(lambda A,B,C,D: (A, B, C, D*10))
    # TODO:
    # This changes the conversion formulas for other PIDs
    # Complicated.

    # (0x50, 4, 'Maximum value for air flow rate from mass air flow sensor',     '0',     '2550',     'g/s',     'A*10, B, C, and D are reserved for future use'),

class x51(PID):
    '''
    0x01 - Gasoline
    0x02 - Methanol
    0x03 - Ethanol
    0x04 - Diesel
    0x05 - LPG
    0x06 - CNG
    0x07 - Propane
    0x08 - Electric
    0x09 - Bifuel running Gasoline
    0x0A - Bifuel running Methanol
    0x0B - Bifuel running Ethanol
    0x0C - Bifuel running LPG
    0x0D - Bifuel running CNG
    0x0E - Bifuel running Prop
    0x0F - Bifuel running Electricity
    0x10 - Bifuel mixed gas/electric
    0x11 - Hybrid gasoline
    0x12 - Hybrid Ethanol
    0x13 - Hybrid Diesel
    0x14 - Hybrid Electric
    0x15 - Hybrid Mixed fuel
    0x16 - Hybrid Regenerative
    '''
    name = 'Fuel Type'
    # TODO

    # (0x52, 1, 'Ethanol fuel %',     '0',     '100',     ' %',     'A*100/255'),

    # (0x53, 2, 'Absolute Evap system Vapor Pressure',     '0',     '327.675',     'kPa',     '1/200 per bit'),

    # (0x54, 2, 'Evap system vapor pressure',     '-32,767',     '32,768',     'Pa',     'A*256+B - 32768'),

    # (0x55, 2, '',     '-100',     '99.22',     ' %',     '(A-128)*100/128\n(B-128)*100/128'),
class x55(PID):
    name = 'Short term secondary oxygen sensor trim bank 1 and bank 3'
    # TODO
    
    # (0x56, 2, 'Long term secondary oxygen sensor trim bank 1 and bank 3',     '-100',     '99.22',     ' %',     '(A-128)*100/128\n(B-128)*100/128'),
class x56(PID):
    name = 'Long term secondary oxygen sensor trim bank 1 and bank 3'
    # TODO
    
    # (0x57, 2, 'Short term secondary oxygen sensor trim bank 2 and bank 4',     '-100',     '99.22',     ' %',     '(A-128)*100/128\n(B-128)*100/128'),

    # (0x58, 2, 'Long term secondary oxygen sensor trim bank 2 and bank 4',     '-100',     '99.22',     ' %',     '(A-128)*100/128\n(B-128)*100/128'),

    # (0x59, 2, 'Fuel rail pressure (absolute)',     '0',     '655,350',     'kPa',     '((A*256)+B) * 10'),
class x59(PID):
    name = 'Fuel rail pressure (absolute)'
    value = prop(lambda A,B: ((A*256)+B) * 10)
    # (0x5A, 1, 'Relative accelerator pedal position',     '0',     '100',     ' %',     'A*100/255'),

    # (0x5B, 1, 'Hybrid battery pack remaining life',     '0',     '100',     ' %',     'A*100/255'),

    # (0x5C, 1, 'Engine oil temperature',     '-40',     '210',     'C',     'A - 40'),

    # (0x5D, 2, 'Fuel injection timing',     '-210.00',     '301.992',     'degrees',     '(((A*256)+B)-26,880)/128'),

    # (0x5E, 2, 'Engine fuel rate',     '0',     '3212.75',     'L/h',     '((A*256)+B)*0.05'),

    # (0x5F, 1, 'Emission requirements to which vehicle is designed',     '',     '',     '',     'Bit Encoded'),

###############################################################################

    # (0x61, 1, 'Drivers demand engine - percent torque',     '-125',     '125',     ' %',     'A-125'),

    # (0x62, 1, 'Actual engine - percent torque',     '-125',     '125',     ' %',     'A-125'),

    # (0x63, 2, 'Engine reference torque',     '0',     '65,535',     'Nm',     'A*256+B'),

    # (0x64, 5, 'Engine percent torque data',     '-125',     '125',     ' %',     'A-125 Idle\nB-125 Engine point 1\nC-125 Engine point 2\nD-125 Engine point 3\nE-125 Engine point 4'),

    # (0x65, 2, 'Auxiliary input / output supported',     '',     '',     '',     'Bit Encoded'),

class x66(PID):
    name = 'Mass air flow sensor'
    @property
    def value(self):
        maf = []
        if self.a & 0x01:
            maf.append(short(self.b, self.c))
        if self.a & 0x02:
            maf.append(short(self.d, self.e))
        return maf


    # TODO

    # (0x67, 3, 'Engine coolant temperature',     '',     '',     '',     ''),

    # (0x68, 7, 'Intake air temperature sensor (UNKNOWN)',
    #     None),

    # (0x69, 7, 'Commanded EGR and EGR Error',     '',     '',     '',     ''),

    # (0x6A, 5, 'Commanded Diesel intake air flow control and relative intake air flow position',     '',     '',     '',     ''),

    # (0x6B, 5, 'Exhaust gas recirculation temperature',     '',     '',     '',     ''),

    # (0x6C, 5, 'Commanded throttle actuator control and relative throttle position',     '',     '',     '',     ''),

    # (0x6D, 6, 'Fuel pressure control system',     '',     '',     '',     ''),

    # (0x6E, 5, 'Injection pressure control system',     '',     '',     '',     ''),

    # (0x6F, 3, 'Turbocharger compressor inlet pressure',     '',     '',     '',     ''),

    # (0x70, 9, 'Boost pressure control',     '',     '',     '',     ''),

    # (0x71, 5, 'Variable Geometry turbo (VGT) control',     '',     '',     '',     ''),

    # (0x72, 5, 'Wastegate control',     '',     '',     '',     ''),

    # (0x73, 5, 'Exhaust pressure',     '',     '',     '',     ''),

    # (0x74, 5, 'Turbocharger RPM',     '',     '',     '',     ''),

    # (0x75, 7, 'Turbocharger temperature',     '',     '',     '',     ''),

    # (0x76, 7, 'Turbocharger temperature',     '',     '',     '',     ''),

    # (0x77, 5, 'Charge air cooler temperature (CACT)',     '',     '',     '',     ''),

    # (0x78, 9, 'Exhaust Gas temperature (EGT) Bank 1',     '',     '',     '',     'Special PID. See below.'),

    # (0x79, 9, 'Exhaust Gas temperature (EGT) Bank 2',     '',     '',     '',     'Special PID. See below.'),

    # (0x7A, 7, 'Diesel particulate filter (DPF)',     '',     '',     '',     ''),

    # (0x7B, 7, 'Diesel particulate filter (DPF)',     '',     '',     '',     ''),

    # (0x7C, 9, 'Diesel Particulate filter (DPF) temperature',     '',     '',     '',     ''),

    # (0x7D, 1, 'NOx NTE control area status',     '',     '',     '',     ''),

    # (0x7E, 1, 'PM NTE control area status',     '',     '',     '',     ''),

    # (0x7F,13, 'Engine run time',     '',     '',     '',     ''),

    # (0x81,21, 'Engine run time for Auxiliary Emissions Control Device(AECD)',     '',     '',     '',     ''),

    # (0x82,21, 'Engine run time for Auxiliary Emissions Control Device(AECD)',     '',     '',     '',     ''),

    # (0x83, 5, 'NOx sensor',     '',     '',     '',     ''),

    # (0x84, 0, 'Manifold surface temperature',     '',     '',     '',     ''),

    # (0x85, 0, 'NOx reagent system',     '',     '',     '',     ''),

    # (0x86, 0, 'Particulate matter (PM) sensor',     '',     '',     '',     ''),

    # (0x87, 0, 'Intake manifold absolute pressure',     '',     '',     '',     ''),
