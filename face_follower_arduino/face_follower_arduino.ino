/*#include <Servo.h>
Servo rotX;
Servo rotY;*/
int Xpos = 0;
int Ypos = 0;
int x = 0;
int y = 0;
String in = "";
boolean isx = true;


void setup() {
  Serial.begin(115200);
  //rotX.attach(2);
  //rotY.attach(3);
}

void loop() {
  while (Serial.available() > 0) {
    char inChar = Serial.read();
    if (isDigit(inChar)) {
      in += inChar;
    } else if (inChar == 'a') {
      x = in.toInt();
      in = "";
    } else if (inChar == 'b') {
      y = in.toInt();
      in = "";
    }
  }
  //==================
  //moving servos because that's what cool guys do TOXLC
  int DXpos = Xpos + x/128;
  int DYpos = Ypos + y/128;
  Xpos = constrain(DXpos, 0, 255);
  Ypos = constrain(DYpos, 0, 255);
  analogWrite(2, Xpos);
  analogWrite(3, Ypos);
  delay(25);
}
