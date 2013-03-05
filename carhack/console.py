import os
import sys
sys.path.insert(0, '.')

import cgitb
cgitb.enable(format='text')

from carapp import app


def main():
    app.load_trips()
    trip = app.trips['2013-03-04_16-39-46']
    trip.recalculate()


if __name__ == '__main__':
    main()
