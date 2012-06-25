OBD-II to DSUB wiring:




Nissan says:
(looking at harness)
---------------------
\  8 7 6 5 4 - - -  /
 \ 16- 141312- - - /
  \---------------/

CAN is 6 and 14?

PG-17: pin 16 is (something about power?)
OBDII standard:
16 +12V
 5 GND
14 CAN_?
 6 CAN_?


            __
        ___/  |
       /      |
12? 16 | o  o | 8 ??
    -  | o  o | 7 ??
CAN 14 | o  o | 6 CAN
 ?? 13 | o  O | 5 GND?
    12 | o  O | 4 ??
     - | o  o | -
     - | o  o | -
     - | o  o | -
       \___   |
           \__|


OBD-II:
Looking at connector

---------------------
\  8 5 4 3 2 - 1 -  /
 \ - 7 6 - - - 9 - /
  \---------------/


Looking at harness


         __
     ___/  |
    /      |
  - | o  o | -
  9 | o  o | 1
  - | o  o | -
  - | o  O | 2
  - | o  O | 3
  6 | o  o | 4
  7 | o  o | 5
  8 | o  o | -
    \___   |
        \__|




DB9
===

Looking at connector
---

 -----------
| 6 5 4 2 3 |
\  8 7 1 9  /
 \---------/

Looking at harness
---

         ______
        /      |
       /     o | 3
     9 | o     |
       |     o | 2
     1 | o     |
       |     o | 4
     7 | o     |
       |     o | 5
     8 | o     |
       \     o | 6
        \______|


CANUSB pinout
---

         ______
        /      |
       /     o | +12v
 GND_1 | o     |
       |     o | CAN_L
 CAN_H | o     |
       |     o | GND_2
     - | o     |
       |     o | -
  +12V | o     |
       \     o | -
        \______|



Summary
=======

CANUSB CAN_H -> 1 -> 7 ???? CAR
CANUSB CAN_L -> 2 -> 5 GND? CAR
CANUSB GND_1 -> 9 -> ---
CANUSB GND_2 -> 4 -> ---


CAR CAN 14 -> --
CAR CAN  6 -> --

Epic fail.

To fix:




