Nissan 370Z CAN-BUS Data
========================


This file is for attempting to reverse engineer the CAN-BUS data
on a 2010 Nissan 370Z.


Data
----

Active IDs with power in ACC or ON:

002
160
180
182
1F9
215
216
245
280
284
285
292
2DE
342
351
354
355
358
35D
385
421
512
54C
551
580
5C5
60D
625
6E2



ID 002 - Unknown
----------------

interval 10ms

IGN ACC: no data

IGN ON:


    (X, Y, 0 or sometimes 1, 7, Z)


* `X` - 127 - 204.
* `Y` - 0 or 255
* `Z` - 16-long repeating sequence

X = 204: -15
X = 203: +17
X = 202: +17
X = 124: +17

?????


* `A` - Steering wheel (wheels?) position lo
* `B` - Steering wheel (wheels?) position hi
    * 227 (full lock left) to 18 (full lock right)

C, D - Power steering pump status?


ID 160 - Unknown
----------------

interval 10ms

Related to engine load/fuel/something

IGN ON:

    (50, 3, 32, 0, 8, 255, 192)
    (61, 85, 217, 0, 8, 255, 224)
    (61, 85, 220, 0, 8, 255, 224)

IGN ENG:

    (A, B, C, D, E, F, G)


* `A`, `B` - sensor data, 16bits
* `C` - sensor data. overflows go to `B`
* `D` - sensor data. typically 0.
* `E` - sensor data. 8, or 224 - G
* `F` - sensor data. typically 255. related to `E` and `F`
* `G` - sensor data. related to `E`. typically 224

Looks like something related to the engine


ID 180 -- Unknown
-----------------

Related to throttle/fuel system.

When IGN in ACC: no data

When IGN in ON:

Sends once:

    (0, 0, 50, 3, 32, 0, 1, 0)

    Sometimes:
    (0, 0, 93, 147, 213, 0, 50, 16)
    (0, 0, 93, 179, 213, 0, 51, 16)


Sends every 10ms:

    (0, 0, 93, 195, 213, 0, X, 16)

where X counts up from 48 to 63 and repeats


    (A, B, C, D, E, F, G, H)

* `A`, `B` Engine RPM.
    * Same as 1F9 C,D
* `F` - Throttle pedal postion, % (F/255 * 100)



ID 182 - Unknown
----------------

Similar to ID 180.

When IGN in ACC: no data

When IGN in ON:

Sends every 10ms:

     (0, 0, 0, 0, 0, X, 0, 245)


where X counts up from 32 to 47 and repeats


Fuel??

H - higher when engine acellerating, cuts out when lifting
B - goes high when lifting


ID 1F9 - Unknown
----------------

When ignition goes from ACC to ON:

    (0, 0, 0, 0, 0, 0, 0, 128) - (repeat every 10ms)


ON:

* `C`, `D` - Engine RPM
    (21, 74) = idle



ID 6E2 - Unknown
----------------

Sends every 100ms:

    (0, 0, 120)
    (0, 0, 121)
    (0, 0, 122)



ID 215 - Unknown
----------------

Sends every 20ms:

    (255, 240, 255, 0, 255, 255)

* `B`
    * 240 - AC LED off
    * 248 - AC LED on


ID 216 - Unknown
----------------

20ms interval

When IGN in ACC:

    (64, 36) - (repeat)


IGN ON:

    (166, 100)

* `A`
    * 100 - CLutch engaged
    * 108 - CLutch *fully* pressed


IGN ACC -> ON:

    (65, 36)
    (65, 36)
    (65, 36)
    (65, 36)
    (64, 100)
    (66, 100) (repeat)



ID 245 - Unknown
----------------

20ms interval

When IGN ON, repeat:

    (255, 224, 0, 24, 0, 0, 255, 224)
    (255, 224, 0, 24, 0, 0, 255, 225)
    (255, 224, 0, 24, 0, 0, 255, 226)
    (255, 224, 0, 24, 0, 0, 255, 227)



ID 280 - Unknown
----------------

20ms interval

When IGN ACC:

    (1, 255, 192, 0, 0, 0, 0, 0) - (repeat)


IGN ACC -> ON:

    (1, 255, 192, 0, 0, 0, 162, 64)

IGN ON:

     (1, X, 192, 0, 0, 0, Y, 64)

* `X` - varies randomly from 13 to 17
* `Y` - varies randomly from 154 to 161


* E, F - vehicle speed


ID 284 - Unknown
----------------

20ms interval

IGN ACC: no data

IGN ON:

    (0, 0, 0, 0, 0, 0, X, Y)

* `X` - counts up from 0 to 255
* `Y` - counts up from 0 to 255, +134 offset from `X`



ID 285 - Unknown
----------------

Same as ID 284. Offset is +135 this time



ID 292 - Unknown
----------------

20ms interval

IGN ACC: no data

IGN ACC -> ON:

    (255, 255, 255, 255, 255, 254, 255, 0)

for 3 seconds

IGN ON:

 (255, 248, X, 128, 15, 254, 0, 0)

* `X` - varies from 60 - 71



ID 2DE - Unknown
----------------

10ms interval

    (0, 0, 128, 5, 240, 0, X, 242)

* `X`
    * 6 when IGN ACC
    * 255 for 20s after ACC -> ON
    * 6 again after


ID 342 - Unknown
----------------

IGN ACC -> ON:

    (3, 35, 162, 246)
    (3, 44, 255, 255)



ID 351 - Unknown
----------------

interval 110ms

IGN ACC:

    (0, 0, 0, 0, 0, 0, 64, 0)


IGN ON:

    (0, 0, 0, 0, 0, 0, 64, 2)
    (0, 0, 0, 0, 0, 64, 64, 2)
    (0, 0, 0, 0, 0, 76, 64, 2) (repeat * 15)
    (0, 0, 0, 0, 0, 12, 64, 2) (repeat)

* `H` - Clutch pedal
    * 2 - Engaged
    * 6 - *fully* pressed


ID 354 - Unknown
----------------

interval 45ms

IGN ACC: no data

IGN ACC -> ON:

    (0, 0, 0, 0, 42, 0, 4, 0)
    (0, 0, 0, 0, 42, 8, 4, 0)
    (0, 0, 0, 0, 42, 16, 4, 0)
    (0, 0, 0, 0, 42, 24, 4, 0)
    (repeat all)

for 3s

IGN ON:

    (0, 0, 0, 0, 0, 0, 4, 0)
    (0, 0, 0, 0, 0, 8, 4, 0)
    (0, 0, 0, 0, 0, 16, 4, 0)
    (0, 0, 0, 0, 0, 24, 4, 0)
    (repeat all)

* `E` - TCS Status
    * 0 - On
    * 64 - Off

* `G`
    * 4 - brake off
    * 20 - brake pedal pressed (little bit)

* `A`,`B` - Speed


ID 355 - Unknown
----------------

interval 45ms

IGN ACC:

    (0, 0, 255, 255, 32, 0, 96)

IGN ON:

    (0, 0, 0, 0, 32, 0, 96)

A,B - Speed
C,D - Speed


ID 358 - Unknown
----------------

interval 110ms

IGN ACC:

    (0, 10, 0, 0, 0, 0, 0, 0)

IGN ACC -> ON:

    (0, 10, 0, 32, 0, 0, 0, 0)
    (4, 10, 0, 32, 0, 0, 0, 0)
    (4, 10, 0, 32, 0, 0, 0, 0)
    (4, 10, 0, 32, 128, 0, 0, 0) (* 10)

IGN ON:

    (4, 10, 0, 32, 0, 0, 0, 0)



ID 35D - Unknown
----------------

interval 110ms

IGN ACC:

    (0, 3, 0, 0, 0, 0, 0, 0)

IGN ON:

    (128, 3, 0, 0, 0, 0, 0, 0)


* `C`
    * 0
    * 64 - wiper pulse
    * 192 - wiper 1 pulse (up)
    * 192 - continuous wiper
    * 224 - fast continuous wiper

* `E`
    * 16 - car stopped
    * 64 - car moving
    * ?? - brake pressed

ID 385 - Unknown
----------------

interval 110ms

IGN ACC & ON

    (4, 0, 0, 0, 0, 0, 0)



ID 421 - 6MT Gear Shift Position Sensor
---------------------------------------

interval 55ms

IGN ACC -> ON

    (128, 1)

IGN ON:

    (X, 65)

* `X` Gear shift position
    * 24 - Neutral
    * 128 - First
    * 136 - Second
    * 144 - Third
    * 152 - Fourth
    * 160 - Fifth
    * 168 - Sixth
    * 16 - Reverse



ID 512 - Unknown
----------------

IGN ACC -> ON:

    (3, 32, 42, 88)
    (3, 44, 255, 255)



ID 54C - Unknown
----------------

interval 110ms

IGN ACC: no data

IGN ON:

    (X, 99, 192, 0, 0, 128, 4, 8)

* `X` - 157 or 158


ID 551 - Unknown
----------------

interval 110ms

IGN ACC: no data

IGN ON:

    (60, 0, 0, 32, 255, 0, 128, 255) - (repeat for 3s)
    (A, B, 0, 160, 255, 0, 128, 255) - (repeat)


* `A` - Sensor data (temp?)
* `B` - Counts up from 0 to 255 (only when engine running)
    * Counts faster at higher RPMs

* `E`
    * 255 - Cruise control master off
    * 254 - Cruise control master on
* `F`
    * 2 - Cruise control master off
    * 82 - Cruise control master on


ID 580 - Unknown
----------------

interval 110ms

IGN ACC: no data

IGN ACC -> ON

    (0, 0, 64, 0, 70)

IGN ON:

    (0, 0, 64, 8, 70)
    (0, 0, 64, 10, 70)
    (0, 0, 64, 12, 70)
    (0, 0, 64, 14, 70)


* `A, B` - Engine RPM
    * (0, 130) = idle (~600rpm)


ID 5C5 - Unknown
----------------

interval 110ms

IGN ACC:

    (128, 0, 76, 156, 0, 12, 0, 127)


IGN ON:

    (68, 0, 76, 156, 0, 12, 0, 127)


* `A` - Parking Brake
    * 68 - On
    * 64 - Off


ID 60D - Body Control Module
----------------------------

interval 110ms

length: 8

Active with IGN ACC, ON

Sample:

    (0, 6, 8, 42, 0, 0, 0, 0)

* `A` - Body Status
    * `A0` - 0
    * `A1` - Headlights on(1)
    * `A2` - Running lights on(1)
    * `A3` - 0
    * `A4` - Driver door open(1)
    * `A5` - Passenger door open(1)
    * `A6` - 0
    * `A7` - 0


* `B` - Turn Signal Status
    * `B0` - 0
    * `B1` - 1
    * `B2` - 1
    * `B3` - 0
    * `B4` - 0
    * `B5` - Left turn signal active(1)
    * `B6` - Right turn signal active(1)
    * `B7` - 0


* `C` - Lock Status
    * `C0` - 0
    * `C1` - 0
    * `C2` - 0
    * `C3` - Driver door locked(1)
    * `C4` - Other locked(1)
    * `C5` - 0
    * `C6` - 0
    * `C7` - 0


* `D` - Unknown
    * Pulses 42 when IGN ACC->ON


ID 625 - Body Control Module
----------------------------

Similar to ID 60D

IGN ACC:

    (2, 0, 255, 14, 32, 0)


IGN ACC -> ON:

    (2, 0, 255, 13, 32, 0)


IGN ON:

    (A, B, 255, 157, 32, 0)


* `A` - Climate Control
    * `A0` - Rear defrost LED on(1)
    * 2 - Idle
    * 4, 6, 8, 10 - Wipers active(?)


* `B` - Body
    * `A0` - 0
    * `A1` - 0
    * `A2` - 0
    * `A3` - 0
    * `A4` - Hi-beams on(1)
    * `A5` - Headlights on(1)
    * `A6` - Running lights on(1)
    * `A7` - AC LED on(1)


ID 6E2 - Unknown
----------------

interval 110ms

IGN ACC: no data

IGN ON:

    (0, 0, 120)
    (0, 0, 121)
    (0, 0, 122)
    (0, 0, 123)








IGN ACC -> ON Sequence
----------------

20121007.164633.983 ID:216
20121007.164634.086 ID:280 Flags:0 Data: (1, 255, 192, 0, 0, 0, 162, 64)
20121007.164634.151 ID:1F9
20121007.164634.151 ID:280 Flags:0 Data: (1, 14, 192, 0, 0, 0, 161, 64)
20121007.164634.174 ID:280 Flags:0 Data: (1, 16, 192, 0, 0, 0, 156, 64)
20121007.164634.194 ID:280 Flags:0 Data: (1, 14, 192, 0, 0, 0, 158, 64)
20121007.164634.213 ID:245
20121007.164634.217 ID:280 Flags:0 Data: (1, 13, 192, 0, 0, 0, 159, 64)
20121007.164634.262 ID:512 Flags:0 Data: (3, 32, 42, 88)
20121007.164634.305 ID:512 Flags:0 Data: (3, 44, 255, 255)


----

20121008.191328.656 ID:60D Flags:0 Data: (6, 6, 0, 42, 0, 0, 0, 0)

20121008.191328.708 ID:5C5 Flags:0 Data: (68, 0, 76, 161, 0, 12, 0, 127)


20121008.191519.726 ID:180 Flags:0 Data: (4, 126, 93, 195, 213, 0, 63, 21)
20121008.191519.904 ID:580 Flags:0 Data: (0, 250, 64, 152, 69)
20121008.191520.016 ID:580 Flags:0 Data: (1, 8, 64, 154, 69)
20121008.191520.126 ID:580 Flags:0 Data: (1, 58, 64, 156, 69)





20121008.191648.293 Stop
