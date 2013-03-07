import os
import sys
sys.path.insert(0, '.')

import cgitb
cgitb.enable(format='text')

from carapp import app


def main():
    trip = app.get_trip('2013-03-05_21-55-07')
    trip.recalculate()


if __name__ == '__main__':
    main()
