#include <Sensirion.h>

#include <DHT_U.h>
#include <DHT.h>

#include <Adafruit_Sensor.h>

#define DHTTYPE DHT22   // Sensor DHT 22  (AM2302)

// SHT71
const uint8_t pinMeetingRoom =  3;            // SHT serial data
const uint8_t pinClkMeetingRoom =  2;       // SHT serial clock
const uint32_t TRHSTEP   = 3000UL;     // Sensor query period
const uint32_t BLINKSTEP =  250UL;     // LED blink period

Sensirion sht = Sensirion(pinMeetingRoom, pinClkMeetingRoom);

uint16_t rawData;
float tempMeetingRoom;
float humMeetingRoom;

byte shtState = 0;

// LM35
int pinLara = 8, pinExternal = 9; // Pino analogico para ligacao do LM35

// Definicoes do sensor : pino, tipo
DHT dhtLara(pinLara, DHTTYPE);
DHT dhtExternal(pinExternal, DHTTYPE);

float tempLara = 0, tempExternal = 0; // Variaveis que armazenam a temperatura em Celsius

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
  dhtLara.begin();
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
            
      // Leitura da umidade
      // float humLara = dhtLara.readHumidity();
      // Leitura da temperatura (Celsius)
      tempLara = dhtLara.readTemperature();
      tempExternal = dhtExternal.readTemperature();
      
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
