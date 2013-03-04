import os
import sys

sys.path.insert(0, '.')
print os.getcwd()
print sys.path


from carapp import app



def main():
    app.load_trips()
    trip = app.trips['2013-03-02_23-41-28']
    series = trip.series['test_sensor.random1']
    for ts, frame in series:
        print frame


if __name__ == '__main__':
    main()
