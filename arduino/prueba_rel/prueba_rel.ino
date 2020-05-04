#include <Servo.h>
#define PIN_SERVO 9

Servo servo;

int incomingByte = 0; // for incoming serial data
int numero = -1;
int bytes[20];

String string;

String leer_string(){
  string = Serial.readString();
  return string;
}

void setup() {
  servo.attach(PIN_SERVO);
  Serial.begin(9600);
  while(!Serial){
    ;
  }
  Serial.setTimeout(20);
  servo.write(1);
}

void loop() {
  string = leer_string();
  numero = string.toInt();
  Serial.print("--->");
  Serial.println(numero,DEC);

  if(numero > 0 && numero < 480){
    int angulo = map(numero, 0, 480,1, 157);
    servo.write(angulo);
  }
}
