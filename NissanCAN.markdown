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

