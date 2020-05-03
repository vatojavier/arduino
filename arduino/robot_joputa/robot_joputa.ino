#include <Servo.h>
#define PIN_SERVO 9

Servo servo;

int incomingByte = 0; // for incoming serial data
int incomingInt = 0;
int bytes[2];

String string;

int leer_int(int n_bytes){

  int numero;


  for(int i = 0; i < 2; i++){
    incomingByte = Serial.read();
    
    
    bytes[i] = incomingByte;
   
  }

  /*Serial.print("Bytes->>");
  Serial.print(bytes[0]);
  Serial.print("/");
  Serial.println(bytes[1]);*/
  
  numero = bytes[0]*255 + bytes[1];
  bytes[0]= 0;
  bytes[1]= 0;
  return numero;
  
  
}

void setup() {
  servo.attach(PIN_SERVO);
  Serial.begin(9600);
  
  Serial.println("Empezando");
  Serial.flush();
}

void loop() {

  if(Serial.available() > 0){
    incomingInt = leer_int(2);
  }else{
    incomingInt = -1;
  }

  Serial.print("numero--->>");
  Serial.println(incomingInt);

//  if(incomingInt > 0){
//    int angulo = map(incomingInt, 0, 300,5, 140);
//    servo.write(angulo);
//  }
  

}
