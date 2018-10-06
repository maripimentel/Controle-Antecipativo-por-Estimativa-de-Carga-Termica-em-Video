float f;

void setup() {

  Serial.begin(9600);

//  pinMode(5, OUTPUT);
}

void loop() {
  if(Serial.available())
      {f=Serial.parseFloat();
        Serial.println(f);
      }
    delay(1000);        
   }

//  recvInfo();
//  lightLED();
//  
//  
//}
//
 
}

 void recvInfo() {

    if (Serial.available() > 0) {

      receivedChar = Serial.read();
      Serial.println(receivedChar);
      newData = true;
    
    }
  }

//void lightLED() {
//
//  int led = (receivedChar - '0');
//
//  while(newData == true) {
//
//    digitalWrite(led, HIGH);
//    Serial.println(data);
//    delay(2000);
//    digitalWrite(led, LOW);
//
//    newData = false;
//    
//  }
  
//}
