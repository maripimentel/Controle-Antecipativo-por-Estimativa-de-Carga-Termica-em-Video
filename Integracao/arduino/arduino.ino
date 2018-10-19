#include <DHT.h>

/* How to use the DHT-22 sensor with Arduino uno
   Temperature and humidity sensor
*/


//Constants
#define DHTPIN 2     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino

// LM35
int pinLara = A0, pinExternal = A1; // Pino analogico para ligacao do LM35

float tempLara = 0, tempExternal = 0; // Variaveis que armazenam a temperatura em Celsius
float samplesLara[8], samplesExternal[8]; // Array para precisão na medição
int i;

// Rele
float f;
char compSignal;
char lastCompSignal;
int rele = 7;
const uint32_t TRHCOM   = 100UL;

// Time
unsigned long curMillis;               // Time interval tracking
unsigned long trhMillis = 0;
unsigned long curMillisCom;               // Time interval tracking
unsigned long trhMillisCom = 0;

void setup()
{
  Serial.begin(9600);                           // Wait at least 11 ms before first cmd
  sht.measTemp(&rawData);              // Maps to: sht.meas(TEMP, &rawData, BLOCK)
  tempMeetingRoom = sht.calcTemp(rawData);
  sht.measHumi(&rawData);              // Maps to: sht.meas(HUMI, &rawData, BLOCK)
  humMeetingRoom = sht.calcHumi(rawData, tempMeetingRoom);
  pinMode(rele, OUTPUT);
  pinMode(pinLara, INPUT);
  pinMode(pinExternal, INPUT);
  logData();
}

void loop()
{
  curMillis = millis();
  curMillisCom = millis();
  
  if (curMillisCom - trhMillisCom >= TRHCOM) {
    compSignal = recvInfo();
    if(lastCompSignal != compSignal) {
      if(compSignal == '1') {
        digitalWrite(rele, LOW);
      }
      else if(compSignal == '0') {
        digitalWrite(rele,HIGH);
      }
    }
    lastCompSignal = compSignal;
    trhMillisCom = curMillisCom;
  }  

  switch (shtState) {
  case 0:
    if (curMillis - trhMillis >= TRHSTEP) {      // Start new temp/humi measurement?
      sht.meas(TEMP, &rawData, NONBLOCK);
      
      for (i = 0; i < 100; i++) {
        tempLara = tempLara + (float(analogRead(pinLara))*5/(1023))/0.01;
        delay(10);
        tempExternal = tempExternal + (float(analogRead(pinExternal))*5/(1023))/0.01;
        delay(10);
      } 
      
      shtState++;
      trhMillis = curMillis;
    }
    break;
  case 1:
    if (sht.measRdy()) {                         // Process temperature measurement?
      tempMeetingRoom = sht.calcTemp(rawData);
      sht.meas(HUMI, &rawData, NONBLOCK);
      shtState++;
    }
    break;
  case 2:
    if (sht.measRdy()) {                         // Process humidity measurement?
      humMeetingRoom = sht.calcHumi(rawData, tempMeetingRoom);
      shtState = 0;
      logData();
    }
    break;
  default:
    //Serial.println("How did I get here?");
    break;
  }
}

void logData() {
  tempLara = tempLara / 100;
  tempExternal = tempExternal / 100;
  
  Serial.print("TM:");   Serial.print(tempMeetingRoom);
  Serial.print("|HM:");  Serial.print(humMeetingRoom);
  Serial.print("|TL:");  Serial.print(tempLara,2);
  Serial.print("|TE:");  Serial.print(tempExternal,2);
  Serial.println();

  delay(100);
  tempLara = 0;
  tempExternal = 0;
 } 

char recvInfo() {
  char received;
  if (Serial.available() > 0) {
    received = Serial.read();
//    Serial.print("Signal Rele: ");
//    Serial.println(received);
  }
  return received;
}
