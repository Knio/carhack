import os
import sys
import time
import cPickle as pickle
import frame

def main():
    fname = sys.argv[1]
    frames = pickle.load(open(fname, 'rb'))
    for frame in frames:
        print frame

if __name__ == '__main__':
    main()
