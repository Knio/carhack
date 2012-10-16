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


    (0x01, 4, 'Monitor status',
        None),

    (0x02, 2, 'DTC that caused required freeze frame data storage',
        None),

    (0x03, 2, 'Fuel system status',
        None),

    (0x04, 1, 'Calculated engine load value (%)',
        lambda A: (A*100/255.)),
        # LOAD_PCT = [current airflow] / [(peak airflow at WOT@STP as a function of rpm) * (BARO/29.92) * SQRT(298/(AAT+273))]
        # Where:
        # - STP = Standard Temperature and Pressure = 25 °C, 29.92 in Hg BARO, SQRT = square root,
        # - WOT = wide open throttle, AAT = Ambient Air Temperature and is in °C
        #
        # Characteristics of LOAD_PCT are:
        # - Reaches 100% at WOT at any altitude, temperature or rpm for both naturally aspirated and boosted engines.
        # - Indicates percent of peak available torque.
        # - Linearly correlated with engine vacuum
        # - Often used to schedule power enrichment.
        # - Compression ignition engines (diesels) shall support this PID using fuel flow in place of airflow for the above calculations.
        #
        # NOTE Both spark ignition and compression ignition engines shall support PID $04. See PID $43 for an additional definition
        # of engine LOAD


    (0x05, 1, 'Engine coolant temperature (C)',
        lambda A: (A-40)),

    # Also bank 3 if two bytes returned
    (0x06, 1, 'Short term fuel trim - Bank 1 (%)',
        lambda A: ((A-128) * 100/128.)),

    # Also bank 3 if two bytes returned
    (0x07, 1, 'Long term fuel trim - Bank 1 (%)',
        lambda A: ((A-128) * 100/128.)),

    # Also bank 4 if two bytes returned
    (0x08, 1, 'Short term fuel trim - Bank 2 (%)',
        lambda A: ((A-128) * 100/128.)),

    # Also bank 4 if two bytes returned
    (0x09, 1, 'Long term fuel trim - Bank 2 (%)',
        lambda A: ((A-128) * 100/128.)),

    (0x0A, 1, 'Fuel rail pressure (kPa g)',
        lambda A: (A*3)),

    (0x0B, 1, 'Intake manifold absolute pressure (kPa)',
        lambda A: (A)),

    (0x0C, 2, 'Engine RPM',
        lambda A,B: (((A*256)+B)/4.)),

    (0x0D, 1, 'Vehicle speed (km/h)',
        lambda A: (A)),

    (0x0E, 1, 'Timing advance (degrees relative to #1 cylinder)',
        lambda A: (A/2. - 64)),

    (0x0F, 1, 'Intake air temperature (C)',
        lambda A: (A-40)),

    (0x10, 2, 'MAF mass air flow rate (g/sec)',
        lambda A,B: (((A*256)+B) / 100)),

    (0x11, 1, 'Absolute throttle position (%)',
        lambda A: (A*100/255.)),

    (0x12, 1, 'Commanded secondary air status',
        None),
        # One bit only set
        # A0 - upstream of first catalytic converter
        # A1 - downstream of first catalytic converter inlet
        # A2 - atmosphere / off

    (0x13, 1, 'Location of oxygen sensors',
        None),
        # A0 - Bank 1 - Sensor 1 present at that location (O2S11)
        # A1 - Bank 1 - Sensor 2 present at that location (O2S12)
        # A2 - Bank 1 - Sensor 3 present at that location (O2S13)
        # A3 - Bank 1 - Sensor 4 present at that location (O2S14)
        # A4 - Bank 2 - Sensor 1 present at that location (O2S21)
        # A5 - Bank 2 - Sensor 2 present at that location (O2S22)
        # A6 - Bank 2 - Sensor 3 present at that location (O2S23)
        # A7 - Bank 2 - Sensor 4 present at that location (O2S24)

    # NOTE:
    # The following PIDs assume that PID 0x13 (above) is supported.
    # If PID 0x1D is supported instead, they have different meanings. :(
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


    (0x1C, 1, 'OBD requirements to which vehicle is designed',
        None),
        # 01 - OBD II (California ARB)
        # 02 - OBD (Federal EPA)
        # 03 - OBD and OBD II
        # 04 - OBD I
        # 05 - Not OBD compliant
        # 06 - EOBD
        # 07 - EOBD and OBD II
        # 08 - EOBD and OBD
        # 09 - EOBD, OBD and OBD II
        # 0A - JOBD
        # 0B - JOBD and OBD II
        # 0C - JOBD and EOBD
        # 0D - JOBD, EOBD, and OBD II

    (0x1D, 1, 'Location of oxygen sensors',
        None),
        # NOTE - Changes the meaning of PIDs 0x14 - 0x1B above

    (0x1E, 1, 'Auxiliary input status',
        None),
        # A1 - Power Take Off (PTO) Status

    (0x1F, 2, 'Run time since engine start (seconds)',
        short),


###############################################################################
    (0x20, 4, 'PIDs supported [21 - 40]',
        None),


    (0x21, 2, 'Distance traveled with malfunction indicator lamp (MIL) on (km)',
        short),

    (0x22, 2, 'Fuel rail pressure (relative to manifold vacuum) (kPa)',
        lambda A,B: (((A*256)+B) * 0.079)),

    (0x23, 2, 'Fuel rail pressure (kPa g)',
        lambda A,B: (((A*256)+B) * 10)),

    # The following PIDs assume that PID 0x13 (above) is supported.
    # If PID 0x1D is supported instead, they have different meanings. :(
    (0x24, 4, 'Wide range oxygen sensor equivalence ratio (lambda), voltage (V) - Bank 1, Sensor 1',
        lambda A,B,C,D:((A*256+B)/32768, 4*(C*256+D)/32768)),

    (0x25, 4, 'Wide range oxygen sensor equivalence ratio (lambda), voltage (V) - Bank 1, Sensor 2',
        lambda A,B,C,D:((A*256+B)/32768, 4*(C*256+D)/32768)),

    (0x26, 4, 'Wide range oxygen sensor equivalence ratio (lambda), voltage (V) - Bank 1, Sensor 3',
        lambda A,B,C,D:((A*256+B)/32768, 4*(C*256+D)/32768)),

    (0x27, 4, 'Wide range oxygen sensor equivalence ratio (lambda), voltage (V) - Bank 1, Sensor 4',
        lambda A,B,C,D:((A*256+B)/32768, 4*(C*256+D)/32768)),

    (0x28, 4, 'Wide range oxygen sensor equivalence ratio (lambda), voltage (V) - Bank 2, Sensor 1',
        lambda A,B,C,D:((A*256+B)/32768, 4*(C*256+D)/32768)),

    (0x29, 4, 'Wide range oxygen sensor equivalence ratio (lambda), voltage (V) - Bank 2, Sensor 2',
        lambda A,B,C,D:((A*256+B)/32768, 4*(C*256+D)/32768)),

    (0x2A, 4, 'Wide range oxygen sensor equivalence ratio (lambda), voltage (V) - Bank 2, Sensor 3',
        lambda A,B,C,D:((A*256+B)/32768, 4*(C*256+D)/32768)),

    (0x2B, 4, 'Wide range oxygen sensor equivalence ratio (lambda), voltage (V) - Bank 2, Sensor 4',
        lambda A,B,C,D:((A*256+B)/32768, 4*(C*256+D)/32768)),

    (0x2C, 1, 'Commanded EGR (%)',
        percent),

    (0x2D, 1, 'EGR Error (%)',
        signed_percent),

    (0x2E, 1, 'Commanded evaporative purge (%)',
        percent),

    (0x2F, 1, 'Fuel level input (%)',
        percent),

    (0x30, 1, 'Number of warm-ups since diagnostic trouble codes cleared',
        lambda A:(A)),
        # A warm-up is defined in the OBD regulations to be sufficient vehicle
        # operation such that coolant temperature rises by at
        # least 22 °C (40 °F) from engine starting and reaches
        # a minimum temperature of 70 °C (160 °F) (60 °C (140 °F) for diesels)

    (0x31, 2, 'Distance traveled since codes cleared (km)',
        short),

    (0x32, 2, 'Evap system vapor pressure (Pa)',
        lambda A,B: (struct.unpack('@h', struct.pack('@BB', A, B))[0]/4.)),

    (0x33, 1, 'Absolute barometric pressure (kPa)',
        lambda A: (A)),

    (0x34, 4, 'Wide range oxygen sensor equivalence ratio (lambda), current (mA) - Bank 1, Sensor 1',
        lambda A,B: (((A*256)+B)/32768., ((C*256)+D)/256. - 128)),

    (0x35, 4, 'Wide range oxygen sensor equivalence ratio (lambda), current (mA) - Bank 1, Sensor 2',
        lambda A,B: (((A*256)+B)/32768., ((C*256)+D)/256. - 128)),

    (0x36, 4, 'Wide range oxygen sensor equivalence ratio (lambda), current (mA) - Bank 1, Sensor 3',
        lambda A,B: (((A*256)+B)/32768., ((C*256)+D)/256. - 128)),

    (0x37, 4, 'Wide range oxygen sensor equivalence ratio (lambda), current (mA) - Bank 1, Sensor 4',
        lambda A,B: (((A*256)+B)/32768., ((C*256)+D)/256. - 128)),

    (0x38, 4, 'Wide range oxygen sensor equivalence ratio (lambda), current (mA) - Bank 2, Sensor 1',
        lambda A,B: (((A*256)+B)/32768., ((C*256)+D)/256. - 128)),

    (0x39, 4, 'Wide range oxygen sensor equivalence ratio (lambda), current (mA) - Bank 2, Sensor 2',
        lambda A,B: (((A*256)+B)/32768., ((C*256)+D)/256. - 128)),

    (0x3A, 4, 'Wide range oxygen sensor equivalence ratio (lambda), current (mA) - Bank 2, Sensor 3',
        lambda A,B: (((A*256)+B)/32768., ((C*256)+D)/256. - 128)),

    (0x3B, 4, 'Wide range oxygen sensor equivalence ratio (lambda), current (mA) - Bank 2, Sensor 4',
        lambda A,B: (((A*256)+B)/32768., ((C*256)+D)/256. - 128)),

    (0x3C, 2, 'Catalyst temperature - Bank 1, Sensor 1 (C)',
        lambda A,B: (((A*256)+B)/10 - 40)),

    (0x3D, 2, 'Catalyst temperature - Bank 2, Sensor 1 (C)',
        lambda A,B: (((A*256)+B)/10 - 40)),

    (0x3E, 2, 'Catalyst temperature - Bank 1, Sensor 2 (C)',
        lambda A,B: (((A*256)+B)/10 - 40)),

    (0x3F, 2, 'Catalyst temperature - Bank 2, Sensor 2 (C)',
        lambda A,B: (((A*256)+B)/10 - 40)),


###############################################################################
    (0x40, 4, 'PIDs supported [41 - 60]',
        None),

    (0x41, 4, 'Monitor status this drive cycle',
        None),
    # The bit in this PID shall report two pieces of information for each monitor:
    #
    # 1)    Monitor enable status for the current driving cycle. This bit shall indicate when a monitor is disabled in a manner such that there is
    #       no way for the driver to operate the vehicle for the remainder of the driving cycle and make the monitor run. Typical examples are:
    #           - Engine-off soak not long enough (e.g., cold start temperature conditions not satisfied),
    #           - Monitor maximum time limit or number of attempts/aborts exceeded,
    #           - Ambient air temperature too low or too high,
    #           - BARO too low (high altitude).
    #       The monitor shall not indicate "disabled" for operator-controlled conditions such as rpm, load, throttle position, minimum time limit
    #       not exceeded, ECT, TP, etc.
    #
    # 2)    Monitor completion status for the current driving/monitoring cycle. Status shall be reset to "not complete" upon starting a new
    #       monitoring cycle. Note that some monitoring cycles can include various engine-operating conditions; other monitoring cycles begin
    #       after the ignition key is turned off. Some status bits on a given vehicle can utilise engine-running monitoring cycles while others can
    #       utilise engine-off monitoring cycles. Resetting the bits to "not complete" upon starting the engine will accommodate most engine-running and engine-off monitoring cycles, however, manufacturers are free to define their own monitoring cycles.
    #
    #       NOTE PID $41 bits shall be utilised for all non-continuous monitors which are supported, and change completion status in PID $01.
    #       If a non-continuous monitor is not supported or always shows "complete", the corresponding PID $41 bits shall indicate disabled
    #       and complete. PID $41 bits may be utilised at the vehicle manufacturer's discretion for all continuous monitors which are supported
    #       with the exception of bit 03 which shall always show CCM (Comprehensive Component Monitoring) as enabled for spark ignition
    #       and compression ignition engines

    #   A - Reserverd (0)

    #   B0 - Misfire monitoring enabled
    #   B1 - Fuel system monitoring enabled
    #   B2 - Comprehensive component monitoring enabled
    #   B3 - Reserverd (0)

    #   B4 - Misfire monitoring complete
    #   B5 - Fuel system monitoring complete
    #   B6 - Comprehensive component monitoring complete
    #   B7 - Reserverd (0)

    #   C0 - Catalyst monitoring enabled
    #   C1 - Heated catalyst monitoring enabled
    #   C2 - Evaporative system monitoring enabled
    #   C3 - Secondary air system monitoring enabled
    #   C4 - A/C system refrigerant monitoring enabled
    #   C5 - Oxygen sensor monitoring enabled
    #   C6 - Oxygen sensor heater monitoring enabled
    #   C7 - EGR system monitoring enabled

    #   D0 - Catalyst monitoring complete
    #   D1 - Heated catalyst monitoring complete
    #   D2 - Evaporative system monitoring complete
    #   D3 - Secondary air system monitoring complete
    #   D4 - A/C system refrigerant monitoring complete
    #   D5 - Oxygen sensor monitoring complete
    #   D6 - Oxygen sensor heater monitoring complete
    #   D7 - EGR system monitoring complete

    (0x42, 2, 'Control module voltage (V)',
        lambda A,B: (((A*256)+B)/1000.)),

    (0x43, 2, 'Absolute load value (%)',
        lambda A,B: (((A*256)+B)*100/255.)),

        # The absolute load value has some different characteristics than the LOAD_PCT defined in PID 04 This definition, although restrictive,
        # will standardise the calculation. LOAD_ABS is the normalised value of air mass per intake stroke displayed as a percent.
        #
        # LOAD_ABS = [air mass (g / intake stroke)] / [1.184 (g / intake stroke) * cylinder displacement in litres]
        #
        # Derivation:
        # - air mass (g / intake stroke) = [total engine air mass (g/sec)] / [rpm (revs/min)* (1 min / 60 sec) * (1/2 # of cylinders (strokes / rev)],
        # - LOAD_ABS = [air mass (g)/intake stroke] / [maximum air mass (g)/intake stroke at WOT@STP at 100% volumetric efficiency] * 100%.
        #
        # Where:
        # - STP = Standard Temperature and Pressure = 25 °C, 29.92 in Hg (101.3 kPa) BARO, WOT = wide open throttle.
        #
        # The quantity (maximum air mass (g)/intake stroke at WOT@STP at 100% volumetric efficiency) is a constant for a given cylinder sw ept
        # volume. The constant is 1.184 (g/litre 3) * cylinder displacement (litre 3/intake stroke) based on air density
        # at STP.
        #
        # Characteristics of LOAD_ABS are:
        # - Ranges from 0 to approximately 0.95 for naturally aspirated engines, 0 – 4 for boosted engines,
        # - Linearly correlated with engine indicated and brake torque,
        # - Often used to schedule spark and EGR rates,
        # - Peak value of LOAD_ABS correlates with volumetric efficiency at WOT.,
        # - Indicates the pumping efficiency of the engine for diagnostic purposes.
        #
        # Spark ignition engine are required to support PID $43. Compression ignition (diesel) engines are not required to support this PID.
        # NOTE  See PID $04 for an additional definition of engine LOAD.

    (0x44, 2, 'Commanded equivalence ratio',
        lambda A,B: (((A*256)+B)/32768.)),
        # Fuel systems that utilise conventional oxygen sensor shall display the commanded open loop equivalence ratio while the fuel control
        # system is in open loop. EQ_RAT shall indicate 1.0 while in closed loop fuel.
        #
        # Fuel systems that utilise wide-range/linear oxygen sensors shall display the commanded equivalence ratio in both open loop and
        # closed loop operation.
        #
        # To obtain the actual A/F ratio being commanded, multiply the stoichiometric A/F ratio by the equivalence ratio. For example, for
        # gasoline, stoichiometric is 14.64:1 ratio. If the fuel control system was commanding an 0.95 EQ_RAT, the commanded A/F ratio to the
        # engine would be 14.64 * 0.95 = 13.9 A/F

        #   < 1.0 - Rich
        #   > 1.0 - Lean

    (0x45, 1, 'Relative throttle position',
        percent),

    (0x46, 1, 'Ambient air temperature',
        lambda A: (A-40)),

    (0x47, 1, 'Absolute throttle position B (%)',
        percent),

    (0x48, 1, 'Absolute throttle position C (%)',
        percent),

    (0x49, 1, 'Accelerator pedal position D (%)',
        percent),

    (0x4A, 1, 'Accelerator pedal position E (%)',
        percent),

    (0x4B, 1, 'Accelerator pedal position F (%)',
        percent),

    (0x4C, 1, 'Commanded throttle actuator (%)',
        percent),

    (0x4D, 2, 'Time run by the engine while MIL activated (minutes)',
        short),

    (0x4E, 2, 'Time since diagnostic trouble codes cleared (minutes)',
        short),

    ####################################
    # 0x4F - 0xFF Reserved by J1979-2002

    (0x4F, 4, 'Maximum value for equivalence ratio, oxygen sensor voltage, oxygen sensor current, and intake manifold absolute pressure (lambda, V, mA, kPa)',
        lambda A,B,C,D: (A, B, C, D*10)),

    # (0x50, 4, 'Maximum value for air flow rate from mass air flow sensor',     '0',     '2550',     'g/s',     'A*10, B, C, and D are reserved for future use'),

    (0x51, 1, 'Fuel Type',
        None),
        #   0x01 - Gasoline
        #   0x02 - Methanol
        #   0x03 - Ethanol
        #   0x04 - Diesel
        #   0x05 - LPG
        #   0x06 - CNG
        #   0x07 - Propane
        #   0x08 - Electric
        #   0x09 - Bifuel running Gasoline
        #   0x0A - Bifuel running Methanol
        #   0x0B - Bifuel running Ethanol
        #   0x0C - Bifuel running LPG
        #   0x0D - Bifuel running CNG
        #   0x0E - Bifuel running Prop
        #   0x0F - Bifuel running Electricity
        #   0x10 - Bifuel mixed gas/electric
        #   0x11 - Hybrid gasoline
        #   0x12 - Hybrid Ethanol
        #   0x13 - Hybrid Diesel
        #   0x14 - Hybrid Electric
        #   0x15 - Hybrid Mixed fuel
        #   0x16 - Hybrid Regenerative

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

    (0x66, 5, 'Mass air flow sensor',
        None),

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

