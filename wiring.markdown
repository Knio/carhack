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
    14 CAN_L
     6 CAN_H


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



Cable:
    ###################################
    ###################################
    ###                             ###
    ###  OBD-II:                    ###
    ###  Looking at connector       ###
    ###                             ###
    ###  ---------------------      ###
    ###  \  6 2 3 5 4 - 8 -  /      ###
    ###   \ - 7 1 - - - 9 - /       ###
    ###    \---------------/        ###
    ###                             ###
    ###                             ###
    ###  Looking at back of harness ###
    ###  ---                        ###

                          __
                      ___/  |
                     /      |
                   - | -  6 | 8
                  15 | 7  2 | 7
         yellow   14 | 1  3 | 6 red
                   - | -  5 | 5 black
                   - | -  4 | 4
                   - | -  - | -
                  10 | 9  8 | 2
                   - | -  - | -
                     \___   |
                         \__|
    ###                             ###
    ###                             ###
    ###                             ###
    ###  DB-9                       ###
    ###  ====                       ###
    ###                             ###
    ###  Looking at connector       ###
    ###  ---                        ###
    ###                             ###
    ###   -----------               ###
    ###  | 1 2 3 4 5 |              ###
    ###  \  6 7 8 9  /              ###
    ###   \---------/               ###
    ###                             ###
    ###  Looking at canusb          ###
    ###  ---                        ###
    ###                             ###
    ###           ______            ###
    ###          /      |           ###
    ###         /     o | 5         ###
    ###       9 | o     |           ###
    ###         |     o | 4 darkred ###
    ###  blue 8 | o     |           ###
    ###         |     o | 3 red     ###
    ###       7 | o     |           ###
    ###         |     o | 2         ###
    ###       6 | o     |           ###
    ###         \     o | 1         ###
    ###          \______|           ###
    ###                             ###
    ###                             ###
    ###                             ###
    ###################################
    ###################################

CANUSB pinout
---

             ______
            /      |
           /     o | 12V_2
     GND_1 | o     |
           |     o | CAN_L
     CAN_H | o     |
           |     o | GND_2
         - | o     |
           |     o | -
     12V_1 | o     |
           \     o | -
            \______|



Summary
=======

    CANUSB CAN_H -> 8 -> 2 -> ---
    CANUSB CAN_L -> 4 -> 4 -> ??? CAR

    CANUSB GND_1 -> 9 -> 10-> ---
    CANUSB GND_2 -> 3 -> 6 -> CAN CAR

    CANUSB 12V_1 -> 6 -> 8 -> ??? CAR
    CANUSB 12V_2 -> 5 -> 5 -> GND CAR


Or, if the CANUSB is looking at the connector:

    CANUSB CAN_H -> 7 -> 15-> --- CAR
    CANUSB CAN_L -> 2 -> 7 -> ??? CAR

    CANUSB GND_1 -> 6 -> 8 -> ??? CAR
    CANUSB GND_2 -> 3 -> 6 -> CAN CAR

    CANUSB 12V_1 -> 9 -> 10-> ---
    CANUSB 12V_2 -> 1 -> 14-> CAN CAR

