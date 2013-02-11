Carhack Design
==============


Features
--------

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
    - live mode: show real-time data from the car as it is bring driven
    - playback mode: view data from previous trips

    Each trip should be independent and have it's own set of data series.
    The app should be able to be run in playback mode only (for running on a
    desktop computer)



* Web Service API:
    - serve some static files (html, js, css)
    - JSON API to:
        - list trips (start time, end time, optional name)
        - list data series in a trip (series name)
        - serve range request to data series in a trip

    - WebSocket API:
        - client subscribes to data series in the currently active trip
        - server pushes data points in real time over the socket


* Web App
    - HTML5 & JS


Design Goals
------------

* Separate data collection (sensor) modules
* Separate data logging modules


Interfaces
----------

* Publisher
    publishes new data points in a series.
    - primary sensors
    - secondary processors
    - log file readers


* Subscriber
    listens on new events
    - secondary processors
    - web service

Publisher and Subscriber only needs to exist
in live mode, and when reprocessing a previous trip

* Log
    stores and retreives time-series data

* Trip
    - live / recorded
    - begin, end time
    - series names

Components
----------

* Core
    - ???

* Sensors : Publisher
    - connect to hardware devices
    - publishes data events

* Data Processors : Subscriber, Publisher
    - read primary data events
    - publish secondary data events

* Web server : Subscriber, LogReader
    - serve static files
    - serve logged data
    - read primary & secondary data events


Problems
--------

- what if user wants to configure sensors at runtime?
- what about request/response type interactions with sensors? (ie obd2, hacking)
