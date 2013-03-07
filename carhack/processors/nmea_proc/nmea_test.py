import cgitb
cgitb.enable(format='text')

import nmea

data = [
    '$GPRMC,055346,V,0,N,0,E,0,0,060313,0,W*5B',
    '$GPVTG,278.9,T,278.9,M,0.0,N,0.0,K,A*23',
    '$GNGSA,A,2,,,,,,,,,,,,,1.2,0.9,0.8*2F',
    '$GPRMC,055548.0,A,4825.908788,N,12319.939277,W,0.0,278.9,060313,,,A*72'
]

def main():
    for i in data:
        obj = nmea.parse(i)
        print
        print obj

    obj = nmea.parse(data[3])
    print obj.latitude
    print obj.longitude


if __name__ == '__main__':
    main()
