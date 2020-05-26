/*
    Sigue posicion de detección de movimiento recibida por serial
*/
#include <Servo.h>

#define PIN_SERVO_H 9
#define PIN_SERVO_V 10

#define READ_TIMEOUT 0

#define MAX_GIRO_H 155
#define MIN_GIRO_H 45

#define MAX_GIRO_V 180
#define MIN_GIRO_V 0

#define IMG_WIDTH 500

String inString[2];    // string to hold input
int indexString = 0;

String string;

int numero = 250;
int angulo_h;
int angulo_v;

Servo servo_h;
Servo servo_v;

String leer_string(){
  
  string = Serial.readString();
  return string;
}


void setup() {
    // put your setup code here, to run once:
    servo_h.attach(PIN_SERVO_H);
    servo_v.attach(PIN_SERVO_V);
    
    servo_h.write(90);
    servo_v.write(90);
    
    Serial.begin(2000000);
    
    while(!Serial){;}
    
    Serial.setTimeout(READ_TIMEOUT);
    
    
    inString[0] = "";
    inString[1] = "";
    
    delay(500);
}

/*x-y\n*/
void loop() {

    while (Serial.available() > 0) {
    int inChar = Serial.read();
    if (isDigit(inChar)) {
      // convert the incoming byte to a char and add it to the string:
      inString[indexString] += (char)inChar;
    }
    // if you get a newline, print the string, then the string's value:
    if(inChar == '-'){
        indexString++;
    }
    if (inChar == '\n') {

        numero = inString[0].toInt();
        angulo_h = map(numero, 20, IMG_WIDTH, MIN_GIRO_H, MAX_GIRO_H);

        numero = inString[1].toInt();
        
        angulo_v = map(numero, 20, IMG_WIDTH, MIN_GIRO_V, MAX_GIRO_V);    

        
        servo_h.write(angulo_h);
        servo_v.write(angulo_v);
        
        // clear the string for new input:
        inString[0] = "";
        inString[1] = "";
        indexString = 0;
    }
  }

    
    

}
