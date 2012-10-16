__all__ = ['PIDS', 'PID']

import struct

percent = \
    lambda A: (A*100/255.)
signed_percent = \
    lambda A: (A*100/255.)
short = \
    lambda A,B: (A * 256 + B)

signed = \
    lambda A: struct.unpack('@b', struct.pack('@B', A))[0]

PIDS = [
###############################################################################
    (0x00, 4, 'PIDs supported [01 - 20]',
        None),


    (0x01, 4, 'Monitor status since DTCs cleared.',
        None),

    (0x02, 2, 'Freeze DTC',
        None),

    (0x03, 2, 'Fuel system status',
        None),

    (0x04, 1, 'Calculated engine load value (%)',
        lambda A: (A*100/255.)),

    (0x05, 1, 'Engine coolant temperature (C)',
        lambda A: (A-40)),

    (0x06, 1, 'Short term fuel trim - Bank 1 (%)',
        lambda A: ((A-128) * 100/128.)),

    (0x07, 1, 'Long term fuel trim - Bank 1 (%)',
        lambda A: ((A-128) * 100/128.)),

    (0x08, 1, 'Short term fuel trim - Bank 2 (%)',
        lambda A: ((A-128) * 100/128.)),

    (0x09, 1, 'Long term fuel trim - Bank 2 (%)',
        lambda A: ((A-128) * 100/128.)),

    (0x0A, 1, 'Fuel pressure (kPa)',
        lambda A: (A*3)),

    (0x0B, 1, 'Intake manifold absolute pressure (kPa)',
        lambda A: (A)),

    (0x0C, 2, 'Engine RPM',
        lambda A,B: (((A*256)+B)/4.)),

    (0x0D, 1, 'Vehicle speed (Km/h)',
        lambda A: (A)),

    (0x0E, 1, 'Timing advance (degrees relative to #1 cylinder)',
        lambda A: (A/2. - 64)),

    (0x0F, 1, 'Intake air temperature (C)',
        lambda A: (A-40)),

    (0x10, 2, 'MAF air flow rate (g/sec)',
        lambda A,B: (((A*256)+B) / 100)),

    (0x11, 1, 'Throttle position (%)',
        lambda A: (A*100/255.)),

    (0x12, 1, 'Commanded secondary air status',
        None),

    (0x13, 1, 'Oxygen sensors present',
        None),

    (0x14, 2, 'Oxygen sensor voltage, Short term fuel trim - Bank 1, Sensor 1',
        lambda A, B: (A/200., (B-128) * 100/128.)),

    (0x15, 2, 'Oxygen sensor voltage, Short term fuel trim - Bank 1, Sensor 2',
        lambda A, B: (A/200., (B-128) * 100/128.)),

    (0x16, 2, 'Oxygen sensor voltage, Short term fuel trim - Bank 1, Sensor 3',
        lambda A, B: (A/200., (B-128) * 100/128.)),

    (0x17, 2, 'Oxygen sensor voltage, Short term fuel trim - Bank 1, Sensor 4',
        lambda A, B: (A/200., (B-128) * 100/128.)),

    (0x18, 2, 'Oxygen sensor voltage, Short term fuel trim - Bank 2, Sensor 1',
        lambda A, B: (A/200., (B-128) * 100/128.)),

    (0x19, 2, 'Oxygen sensor voltage, Short term fuel trim - Bank 2, Sensor 2',
        lambda A, B: (A/200., (B-128) * 100/128.)),

    (0x1A, 2, 'Oxygen sensor voltage, Short term fuel trim - Bank 2, Sensor 3',
        lambda A, B: (A/200., (B-128) * 100/128.)),

    (0x1B, 2, 'Oxygen sensor voltage, Short term fuel trim - Bank 2, Sensor 4',
        lambda A, B: (A/200., (B-128) * 100/128.)),


    (0x1C, 1, 'OBD Standards',
        None),

    (0x1D, 1, 'Oxygen sensors present',
        None),

    (0x1E, 1, 'Auxiliary input status',
        None),

    (0x1F, 2, 'Run time since engine start (seconds)',
        short),


###############################################################################
    (0x20, 4, 'PIDs supported [21 - 40]',
        None),


    (0x21, 2, 'Distance traveled with malfunction indicator lamp (MIL) on (km)',
        short),

    (0x22, 2, 'Fuel Rail Pressure (relative to manifold vacuum) (kPa)',
        lambda A,B: (((A*256)+B) * 0.079)),

    (0x23, 2, 'Fuel Rail Pressure (diesel, or gasoline direct inject) (kPa)',
        lambda A,B: (((A*256)+B) * 10)),

    (0x24, 4, 'O2S1_WR_lambda(1): Equivalence Ratio, Voltage (V)',
        None),

    (0x25, 4, 'O2S2_WR_lambda(1): Equivalence Ratio, Voltage (V)',
        None),

    (0x26, 4, 'O2S3_WR_lambda(1): Equivalence Ratio, Voltage (V)',
        None),

    (0x27, 4, 'O2S4_WR_lambda(1): Equivalence Ratio, Voltage (V)',
        None),

    (0x28, 4, 'O2S5_WR_lambda(1): Equivalence Ratio, Voltage (V)',
        None),

    (0x29, 4, 'O2S6_WR_lambda(1): Equivalence Ratio, Voltage (V)',
        None),

    (0x2A, 4, 'O2S7_WR_lambda(1): Equivalence Ratio, Voltage (V)',
        None),

    (0x2B, 4, 'O2S8_WR_lambda(1): Equivalence Ratio, Voltage (V)',
        None),

    (0x2C, 1, 'Commanded EGR (%)',
        percent),

    (0x2D, 1, 'EGR Error',
        signed_percent),

    (0x2E, 1, 'Commanded evaporative purge (%)',
        percent),

    (0x2F, 1, 'Fuel Level Input (%)',
        percent),

    (0x30, 1, '# of warm-ups since codes cleared',
        lambda A:(A)),

    (0x31, 2, 'Distance traveled since codes cleared (km)',
        short),

    (0x32, 2, 'Evap. System Vapor Pressure (Pa)',
        lambda A,B: (struct.unpack('@h', struct.pack('@BB', A, B))[0]/4.)),

    (0x33, 1, 'Barometric pressure (kPa)',
        lambda A: (A)),

    (0x34, 4, 'O2S1_WR_lambda(1):Equivalence Ratio, Current (mA)',
        lambda A,B: (((A*256)+B)/32768., ((C*256)+D)/256. - 128)),

    (0x35, 4, 'O2S2_WR_lambda(1):Equivalence Ratio, Current (mA)',
        lambda A,B: (((A*256)+B)/32768., ((C*256)+D)/256. - 128)),

    (0x36, 4, 'O2S3_WR_lambda(1):Equivalence Ratio, Current (mA)',
        lambda A,B: (((A*256)+B)/32768., ((C*256)+D)/256. - 128)),

    (0x37, 4, 'O2S4_WR_lambda(1):Equivalence Ratio, Current (mA)',
        lambda A,B: (((A*256)+B)/32768., ((C*256)+D)/256. - 128)),

    (0x38, 4, 'O2S5_WR_lambda(1):Equivalence Ratio, Current (mA)',
        lambda A,B: (((A*256)+B)/32768., ((C*256)+D)/256. - 128)),

    (0x39, 4, 'O2S6_WR_lambda(1):Equivalence Ratio, Current (mA)',
        lambda A,B: (((A*256)+B)/32768., ((C*256)+D)/256. - 128)),

    (0x3A, 4, 'O2S7_WR_lambda(1):Equivalence Ratio, Current (mA)',
        lambda A,B: (((A*256)+B)/32768., ((C*256)+D)/256. - 128)),

    (0x3B, 4, 'O2S8_WR_lambda(1):Equivalence Ratio, Current (mA)',
        lambda A,B: (((A*256)+B)/32768., ((C*256)+D)/256. - 128)),

    (0x3C, 2, 'Catalyst Temperature - Bank 1, Sensor 1 (C)',
        lambda A,B: (((A*256)+B)/10 - 40)),

    (0x3D, 2, 'Catalyst Temperature - Bank 2, Sensor 1 (C)',
        lambda A,B: (((A*256)+B)/10 - 40)),

    (0x3E, 2, 'Catalyst Temperature - Bank 1, Sensor 2 (C)',
        lambda A,B: (((A*256)+B)/10 - 40)),

    (0x3F, 2, 'Catalyst Temperature - Bank 2, Sensor 2 (C)',
        lambda A,B: (((A*256)+B)/10 - 40)),


###############################################################################
    (0x40, 4, 'PIDs supported [41 - 60]',
        None),

    (0x41, 4, 'Monitor status this drive cycle',
        None),

    (0x42, 2, 'Control module voltage (V)',
        lambda A,B: (((A*256)+B)/1000.)),

    (0x43, 2, 'Absolute load value (%)',
        lambda A,B: (((A*256)+B)*100/255.)),

    (0x44, 2, 'Command equivalence ratio',
        lambda A,B: (((A*256)+B)/32768.)),

    (0x45, 1, 'Relative throttle position',
        lambda A: (A*100/255)),

    (0x46, 1, 'Ambient air temperature',
        lambda A: (A-40)),

    (0x47, 1, 'Absolute throttle position B (%)',
        lambda A: (A*100/255)),

    (0x48, 1, 'Absolute throttle position C (%)',
        lambda A: (A*100/255)),

    (0x49, 1, 'Accelerator pedal position D (%)',
        lambda A: (A*100/255)),

    (0x4A, 1, 'Accelerator pedal position E (%)',
        lambda A: (A*100/255)),

    (0x4B, 1, 'Accelerator pedal position F (%)',
        lambda A: (A*100/255)),

    (0x4C, 1, 'Commanded throttle actuator (%)',
        lambda A: (A*100/255)),

    (0x4D, 2, 'Time run with MIL on (minutes)',
        lambda A,B: ((A*256)+B)),

    (0x4E, 2, 'Time since trouble codes cleared',
        lambda A,B: ((A*256)+B)),

    (0x4F, 4, 'Maximum value for equivalence ratio, oxygen sensor voltage, oxygen sensor current, and intake manifold absolute pressure (V, mA, kPa)', 
        lambda A,B,C,D: (A, B, C, D*10)),

    # (0x50, 4, 'Maximum value for air flow rate from mass air flow sensor',     '0',     '2550',     'g/s',     'A*10, B, C, and D are reserved for future use'),

    # (0x51, 1, 'Fuel Type',     '',     '',     '',     'From fuel type table see below'),

    # (0x52, 1, 'Ethanol fuel %',     '0',     '100',     ' %',     'A*100/255'),

    # (0x53, 2, 'Absolute Evap system Vapor Pressure',     '0',     '327.675',     'kPa',     '1/200 per bit'),

    # (0x54, 2, 'Evap system vapor pressure',     '-32,767',     '32,768',     'Pa',     'A*256+B - 32768'),

    # (0x55, 2, 'Short term secondary oxygen sensor trim bank 1 and bank 3',     '-100',     '99.22',     ' %',     '(A-128)*100/128\n(B-128)*100/128'),

    # (0x56, 2, 'Long term secondary oxygen sensor trim bank 1 and bank 3',     '-100',     '99.22',     ' %',     '(A-128)*100/128\n(B-128)*100/128'),

    # (0x57, 2, 'Short term secondary oxygen sensor trim bank 2 and bank 4',     '-100',     '99.22',     ' %',     '(A-128)*100/128\n(B-128)*100/128'),

    # (0x58, 2, 'Long term secondary oxygen sensor trim bank 2 and bank 4',     '-100',     '99.22',     ' %',     '(A-128)*100/128\n(B-128)*100/128'),

    # (0x59, 2, 'Fuel rail pressure (absolute)',     '0',     '655,350',     'kPa',     '((A*256)+B) * 10'),

    # (0x5A, 1, 'Relative accelerator pedal position',     '0',     '100',     ' %',     'A*100/255'),

    # (0x5B, 1, 'Hybrid battery pack remaining life',     '0',     '100',     ' %',     'A*100/255'),

    # (0x5C, 1, 'Engine oil temperature',     '-40',     '210',     'C',     'A - 40'),

    # (0x5D, 2, 'Fuel injection timing',     '-210.00',     '301.992',     'degrees',     '(((A*256)+B)-26,880)/128'),

    # (0x5E, 2, 'Engine fuel rate',     '0',     '3212.75',     'L/h',     '((A*256)+B)*0.05'),

    # (0x5F, 1, 'Emission requirements to which vehicle is designed',     '',     '',     '',     'Bit Encoded'),

###############################################################################
    (0x60, 4, 'PIDs supported [61 - 80]',
        None),

    # (0x61, 1, 'Drivers demand engine - percent torque',     '-125',     '125',     ' %',     'A-125'),

    # (0x62, 1, 'Actual engine - percent torque',     '-125',     '125',     ' %',     'A-125'),

    # (0x63, 2, 'Engine reference torque',     '0',     '65,535',     'Nm',     'A*256+B'),

    # (0x64, 5, 'Engine percent torque data',     '-125',     '125',     ' %',     'A-125 Idle\nB-125 Engine point 1\nC-125 Engine point 2\nD-125 Engine point 3\nE-125 Engine point 4'),

    # (0x65, 2, 'Auxiliary input / output supported',     '',     '',     '',     'Bit Encoded'),

    # (0x66, 5, 'Mass air flow sensor',     '',     '',     '',     ''),

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

###############################################################################
    (0x80, 4, 'PIDs supported [81 - A0]',
        None),

    # (0x81,21, 'Engine run time for Auxiliary Emissions Control Device(AECD)',     '',     '',     '',     ''),

    # (0x82,21, 'Engine run time for Auxiliary Emissions Control Device(AECD)',     '',     '',     '',     ''),

    # (0x83, 5, 'NOx sensor',     '',     '',     '',     ''),

    # (0x84, 0, 'Manifold surface temperature',     '',     '',     '',     ''),

    # (0x85, 0, 'NOx reagent system',     '',     '',     '',     ''),

    # (0x86, 0, 'Particulate matter (PM) sensor',     '',     '',     '',     ''),

    # (0x87, 0, 'Intake manifold absolute pressure',     '',     '',     '',     ''),

###############################################################################
    (0xA0, 4, 'PIDs supported [A1 - C0]',
        None),

###############################################################################
    (0xC0, 4, 'PIDs supported [C1 - E0]',
        None),

]

from collections import namedtuple

PIDType = namedtuple('PID', ['pid', 'length', 'desc', 'func'])

PID = {}

for pid, length, desc, func in PIDS:
    PID[pid] = PIDType(pid=pid, length=length, desc=desc, func=func)

