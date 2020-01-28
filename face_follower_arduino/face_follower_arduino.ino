#include <Servo.h>
Servo rotX;
Servo rotY;
int Xpos = 0;
int Ypos = 0;
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
      Xpos = in.toInt();
      in = "";
    }
    if (inChar == '\n') {
      Ypos = in.toInt();
      in = "";
    }
  }
  //==================
  //moving servos because that's what cool guys do
  rotX.write(rotX.read()+(Xpos-256)/64);
  rotY.write(rotY.read()+(Ypos-256)/64);
  
}
