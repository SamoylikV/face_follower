#include <Servo.h>
Servo rotX;
Servo rotY;
int xpos = 0;
int ypos = 0;
String in = "";
boolean isx = true;


void setup() {
  Serial.begin(115200);
  rotX.attach(9);
  rotY.attach(10);
}

void loop() {
  while (Serial.available() > 0) {
      int inChar = Serial.read();
    if (isDigit(inChar)) {
      in += (char)inChar;
    }
    if (inChar == '_') {
      Xpos = in.toInt());
      in = "";
    }
    if (inChar == '\n') {
      Ypos = in.toInt());
      in = "";
    }
  }
}
