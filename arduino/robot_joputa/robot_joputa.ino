#include <Servo.h>
#define PIN_SERVO 9
#define READ_TIMEOUT 0
#define VELOCIDAD 4

Servo servo;

int numero = 0;
int angulo;
int actual;

int pm = 240;

String string;

String leer_string(){
  
  string = Serial.readString();
  return string;
}

void setup() {
  servo.attach(PIN_SERVO);
  Serial.begin(250000);
  while(!Serial){
    ;
  }
  Serial.setTimeout(READ_TIMEOUT);
  servo.write(90);
  delay(500);
}

void loop() {
  string = leer_string();
  numero = string.toInt();
  actual = servo.read();

  if(numero == 1 && actual > 1){
    servo.write(actual-VELOCIDAD);
  }else if(numero == 3 && actual < 155){
    servo.write(actual+VELOCIDAD);
  }


}
