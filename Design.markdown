Carhack Design
--------------

* Record data from various sensors in the car

* All data should be in the form of snapshots of a sensor value in a time-series
    - series name
    - timestamp (should be fairly precise)
    - data (in various formats)

    TODO: can we think of any sensors that won't fit in this format?

* Two types of data series:
    - primary series: "raw" values from the sensors
        Examples:
            - CANBUS frames
            - accelerometer, gyro, compass, gps readings
    - secondary series: "processed" data that is derived from primary data
        Examples:
            - Coolant temperature (parsed from CANBUS frames)
            - Kalman filtered position, orientation, and acceleration values
                (calculated from multiple sensors)

    Primary data should be stored on disk as it cannot easily be regenerated.
    Secondary data can be derived from the primary data, and need not be stored
    (but we still might want to store it for efficiency)

    Primary data can be stored in append-only structures

    Secondary data should be able to be generated either in real-time as primary
    data is collected, or as a post-process (because we don't want to have to
    go drive around again every time we reverse engineer another sensor or
    tweak an algorithm)

    Real-time secondary data generation could lag behind the primary data,
    or be mutable and modify previous data points


* Two modes of operation:
    - live mode:






























