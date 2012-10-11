CarHack
=======

Car Computer project to interface with a car over CAN-BUS.


CANUSB
------

CANUSB Adapter: http://canusb.com

Tested on `Win XP 32bit` (works) and `Win 7 64bit` (works, using 32bit python)


* Install Python (tested with 2.7) 32bit
    * Install setuptools
    * Install pip
    * Install tornado
    * Install pyy


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


Data
----

https://ting.com/devices/SierraU250



Music
-----

USB -> 6ch analog out wired to amp
