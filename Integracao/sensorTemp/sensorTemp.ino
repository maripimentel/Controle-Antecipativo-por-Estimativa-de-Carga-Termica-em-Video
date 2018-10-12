#include <Sensirion.h>

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
int pinLara = A0, pinExternal = A1; // Pino analogico para ligacao do LM35

// Variaveis que armazenam a temperatura em Celsius
float tempLara = 0, tempExternal;
float samplesLara[8], samplesExternal[8]; // Array para precisão na medição
int i;


// Time
unsigned long curMillis;               // Time interval tracking
unsigned long trhMillis = 0;
unsigned long blinkMillis = 0;


void setup()
{
  Serial.begin(9600);                           // Wait at least 11 ms before first cmd
  sht.measTemp(&rawData);              // Maps to: sht.meas(TEMP, &rawData, BLOCK)
  tempMeetingRoom = sht.calcTemp(rawData);
  sht.measHumi(&rawData);              // Maps to: sht.meas(HUMI, &rawData, BLOCK)
  humMeetingRoom = sht.calcHumi(rawData, tempMeetingRoom);
  logData();
}

void loop()
{
  curMillis = millis();

  switch (shtState) {
  case 0:
    if (curMillis - trhMillis >= TRHSTEP) {      // Start new temp/humi measurement?
      sht.meas(TEMP, &rawData, NONBLOCK);
      
      for(i = 0;i<=7;i++){ // Loop que faz a leitura da temperatura 8 vezes
        samplesLara[i] = ( 5.0 * analogRead(pinLara) * 100.0) / 1024.0;
        samplesExternal[i] = ( 5.0 * analogRead(pinExternal) * 100.0) / 1024.0;
        
        //A cada leitura, incrementa o valor da variavel tempc
        tempLara = tempLara + samplesLara[i];
        tempExternal = tempExternal + samplesExternal[i]; 
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
    Serial.println("How did I get here?");
    break;
  }
}

void logData() {
  Serial.print("Temp MeetingRoom: ");   Serial.print(tempMeetingRoom);
  Serial.print(" *C, Hum MeetingRoom: ");  Serial.print(humMeetingRoom);
  Serial.println(" %");
  
  // Divide a variavel tempc por 8, para obter precisão na medição
  tempLara = tempLara/8.0;
  tempExternal = tempExternal/8.0;
  
  Serial.print("Temp Lara: ");
  Serial.print(tempLara,2);
  Serial.println("*C ");
  Serial.print("Temp External: ");
  Serial.print(tempExternal,2);
  Serial.println("*C ");
  Serial.println("****************************");
  
  tempLara = 0;
  tempExternal = 0;
} 
