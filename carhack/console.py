import os
import sys
sys.path.insert(0, '.')

import cgitb
cgitb.enable(format='text')

from carapp import app


def main():
    trip = app.get_trip('2013-03-11_15-47-49')
    trip.recalculate()



if __name__ == '__main__':
    main()
