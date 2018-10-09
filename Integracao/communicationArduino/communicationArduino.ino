float f;
char compSignal

void setup() {

  Serial.begin(9600);
  rele = pinMode(5, OUTPUT);
}

void loop() {
   compSignal = recvInfo();
   if(compSignal == 'l') {
     digitalWrite(rele, LOW)
   }
   else if(compSignal == 'l') {
     digitalWrite(rele,HIGH)
   }
   
   delay(100)
}

 char recvInfo() {
    if (Serial.available() > 0) {
      received = Serial.read();
      Serial.println(received);
    }
    return received;
  }

