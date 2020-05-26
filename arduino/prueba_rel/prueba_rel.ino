String string;
char cadena[10];
char * pch;

int numero;

String leer_string(){
  string = Serial.readString();
  return string;
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  while(!Serial){
    ;
  }
  Serial.setTimeout(2);
}

void loop() {
    
   if(Serial.available() > 0){
        string = leer_string();
        numero = string.toInt();

          digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
          delay(numero);                       // wait for a second
          digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
          delay(numero);                       // wait for a 
    }
    
}
