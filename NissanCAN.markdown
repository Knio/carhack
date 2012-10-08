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



ID 355 - Unknown
----------------

interval 45ms

IGN ACC:

    (0, 0, 255, 255, 32, 0, 96)

IGN ON:

    (0, 0, 0, 0, 32, 0, 96)



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






ID 385 - Unknown
----------------

interval 110ms

IGN ACC & ON

    (4, 0, 0, 0, 0, 0, 0)



ID 421 - 6MT Gear Shift Position
--------------------------------

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
    (60, 0, 0, 160, 255, 0, 128, 255) - (repeat)


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


ID 5C5 - Unknown
----------------

interval 110ms

IGN ACC:

    (128, 0, 76, 156, 0, 12, 0, 127)


IGN ON:

    (68, 0, 76, 156, 0, 12, 0, 127)



ID 60D - Headlight Select Request
------------------------

interval 110ms

IGN ACC:

    (0, 2, 8, 0, 0, 0, 0, 0)

IGN ACC -> ON:

    (0, 6, 8, 0, 0, 0, 0, 0)
    (0, 6, 8, 42, 0, 0, 0, 0)


IGN ON:

    (X, 6, 8, 0, 0, 0, 0, 0)

* `X` - Headlight select
    * 0 - Auto
    * 4 - DRL
    * 6 - On


ID 625 - Headlight Select Response
----------------

Similar to ID 60D

IGN ACC:

    (2, 0, 255, 14, 32, 0)


IGN ACC -> ON:

    (2, 0, 255, 13, 32, 0)


IGN ON:

    (2, X, 255, 157, 32, 0)

* `X` - Headlight select
    * 0 - Auto
    * 64 - DRL
    * 96 - On




ID 6E2 - Unknown
----------------

interval 110ms

IGN ACC: no data

IGN ON:

    (0, 0, 120)
    (0, 0, 121)
    (0, 0, 122)
    (0, 0, 123)



