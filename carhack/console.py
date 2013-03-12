import os
import sys
sys.path.insert(0, '.')

import cgitb
cgitb.enable(format='text', context=10)

from carapp import app

def main():
    trip = app.get_trip('2013-03-11_18-31-10')
    trip.recalculate()

    trip = app.get_trip('2013-03-11_19-02-40')
    trip.recalculate()

if __name__ == '__main__':
    main()
