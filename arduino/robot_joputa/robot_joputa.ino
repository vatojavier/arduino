#include <Servo.h>
#define PIN_SERVO 9
#define READ_TIMEOUT 10

Servo servo;

int numero = -1;
int angulo;

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
  Serial.setTimeout(READ_TIMEOUT);
  servo.write(1);
}

void loop() {
  string = leer_string();
  numero = string.toInt();
//  Serial.print("--->");
//  Serial.println(numero,DEC);

  if(numero > 0 && numero < 480){
    angulo = map(numero, 0, 480,1, 157);
    servo.write(angulo);
  }
}
