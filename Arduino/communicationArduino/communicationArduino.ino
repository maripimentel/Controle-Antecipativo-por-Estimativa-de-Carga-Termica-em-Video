char receivedChar;
boolean newData = false;
String data = "OI!";

void setup() {

  Serial.begin(9600);

  pinMode(5, OUTPUT);
}

void loop() {

  recvInfo();
  lightLED();
  
  
}

void recvInfo() {

  if (Serial.available() > 0) {

    receivedChar = Serial.read();
    newData = true;
    
  }
  
}

void lightLED() {

  int led = (receivedChar - '0');

  while(newData == true) {

    digitalWrite(led, HIGH);
    Serial.println(data);
    delay(2000);
    digitalWrite(led, LOW);

    newData = false;
    
  }
  
}
