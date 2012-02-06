#include <Arduino.h>

class LED {
  public:
    //void setup() {
    LED() {
      // initialize the digital pin as an output.
      // Pin 13 has an LED connected on most Arduino boards:
      pinMode(13, OUTPUT);
    }
    void loop() {
      digitalWrite(13, HIGH);
      delay(1000);
      digitalWrite(13, LOW);
      delay(500);
    }
};


