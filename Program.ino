/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
int x;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1);
  myservo.attach(9);
}

void loop(){
  while (!Serial.available());
   x = Serial.readString().toInt();
   Serial.print(x);
   if(x == 0){
      pos = 0;
   }
   else if (x == 1){
      pos = 180;
   }
   myservo.write(pos);
   
}
