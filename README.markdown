CarHack
=======

Car Computer project to interface with a car over CAN-BUS.


Related products
----------------

* OpenXC http://openxcplatform.com/
* RaceLogic



CANUSB
------

CANUSB Adapter: http://canusb.com

Tested on `Win XP 32bit` (works) and `Win 7 64bit` (works, using 32bit python)

* Buy a CANUSB adapter

* Buy an OBD2 to DB9 cable
    * https://www.sparkfun.com/products/10087 works
        * But you have to rewire it. See `wiring.markdown`

* Install Python (tested with 2.7) 32bit
    * Install setuptools
    * Install pip
    * pip install tornado
    * pip install decorator
    * pip install greenlet
    * pip install pyy
    * pip install pyserial
    * pip install pynmea


* Install CANUSB FTDI Drivers
  * plug in CANUSB and when windows fails to install it, tell it to look in the `CDM_2.08.14_CANUSB` folder


* Install CANUSM D2XX DLL
  * run canusbdrv018.exe


* Files can also be found at http://canusb.com/downloads.htm


WebCam
------

http://videocapture.sourceforge.net/

http://www.lfd.uci.edu/~gohlke/pythonlibs/#pil

    from VideoCapture import Device
    cam = Device();
    cam.saveSnapshot('image.jpg')



Accellerometer
--------------

http://tech.yostengineering.com/3-space-sensor/product-family/embedded

Solder on a USB plug and use over a virtual COM port


GPS
---

None yet :(


Music
-----

USB -> 6ch analog out wired to amp
