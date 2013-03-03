from carapp import app

def main():
    app.load_trips()
    trip = app.trips['2013-03-02_00-40-46']
    series = trip.series['canusb.can.421']
    for ts, frame in series:
        print frame


if __name__ == '__main__':
    main()
