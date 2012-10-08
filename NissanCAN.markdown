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
29



ID 002 - Unknown
----------------

Sends every 10ms:

    (124, 255, 0, 7, 12)
    (124, 255, 0, 7, 29)
    (124, 255, 0, 7, 46)
    (124, 255, 0, 7, 63)
    (124, 255, 0, 7, 192)
    (124, 255, 0, 7, 209)
    (124, 255, 0, 7, 226)
    (124, 255, 0, 7, 243)
    (124, 255, 0, 7, 132)
    (124, 255, 0, 7, 149)
    (124, 255, 0, 7, 166)
    (124, 255, 0, 7, 183)
    (124, 255, 0, 7, 72)
    (124, 255, 0, 7, 89)
    (124, 255, 0, 7, 106)
    (124, 255, 0, 7, 123)



ID 160 - Unknown
----------------

When ignition goes from ACC to ON:

    (50, 3, 32, 0, 8, 255, 192)
    (61, 85, 217, 0, 8, 255, 224)
    (61, 85, 220, 0, 8, 255, 224)  - (repeat every 10ms)



ID 180 -- Unknown
-----------------

When IGN in ACC: no data

When IGN in ON:

Sends once:

    (0, 0, 50, 3, 32, 0, 1, 0)


Sends every 10ms:

    (0, 0, 93, 195, 213, 0, X, 16)

where X counts up from 48 to 63 and repeats



ID 182 - Unknown
----------------

Similar to ID 180.

When IGN in ACC: no data

When IGN in ON:

Sends every 10ms:

     (0, 0, 0, 0, 0, X, 0, 245)


where X counts up from 32 to 47 and repeats



ID 1F9 - Unknown
----------------

When ignition goes from ACC to ON:

    (0, 0, 0, 0, 0, 0, 0, 128) - (repeat every 10ms)



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



ID 216 - Unknown
----------------

20ms interval

When IGN in ACC:

    (64, 36) - (repeat)


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



ID 284 - Unknown
----------------

20ms interval

IGN ACC: no data

IGN ON:

    (0, 0, 0, 0, 0, 0, X, Y)

* `X` - counts up from 0 to 255
* `Y` - counts up from 0 to 255, +134 offset from `Y`



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







































