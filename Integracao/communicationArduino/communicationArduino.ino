float f;
char compSignal;
int rele = 7;

void setup() {
  Serial.begin(9600);
  pinMode(rele, OUTPUT);
}

void loop() {
  compSignal = recvInfo();
  if(compSignal == 'l') {
    digitalWrite(rele, LOW);
  }
  else if(compSignal == 'l') {
    digitalWrite(rele,HIGH);
  }
   
  delay(100);
}

char recvInfo() {
  char received;
  if (Serial.available() > 0) {
    received = Serial.read();
    Serial.println(received);
  }
  return received;
}

