import os
import sys
import time
import pycanusb
import cPickle as pickle
from ctypes import *


def main():
    fname = sys.argv[1]
    frames = pickle.load(open(fname, 'rb'))
    print frames


if __name__ == '__main__':
    main()
