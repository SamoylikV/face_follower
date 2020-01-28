#include <Servo.h>
Servo rotX;
Servo rotY;
int Xpos = 0;
int Ypos = 0;
String in = "";
boolean isx = true;


void setup() {
  Serial.begin(115200);
  rotX.attach(2);
  rotY.attach(3);
}

void loop() {
  while (Serial.available() > 0) {
      char inChar = Serial.read();
    if (isDigit(inChar)) {
      in += inChar;
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
  int newXpos = min(max((rotX.read()+(Xpos-256)/256), 0), 180);
  Serial.print(newXpos);
  Serial.print('-');
  Serial.println(); 
  rotX.write(newXpos);
  rotY.write(rotY.read()+(Ypos-256)/64);
  delay(25);
}
