/*
 * Example code for SHT1x or SHT7x sensors demonstrating blocking calls
 * for temperature and humidity measurement in the setup routine and
 * non-blocking calls in the main loop.  The pin 13 LED is flashed as a
 * background task while temperature and humidity measurements are made.
 * In addition, the sensor may be placed in low resolution mode by
 * uncommenting the status register write call in setup().
 */

#include <Sensirion.h>

const uint8_t dataPin =  2;            // SHT serial data
const uint8_t sclkPin =  3;            // SHT serial clock
const uint8_t dataPin2 =  4;            // SHT serial data
const uint8_t sclkPin2 =  5;            // SHT serial clock
const uint32_t TRHSTEP   = 3000UL;     // Sensor query period

Sensirion sht = Sensirion(dataPin, sclkPin);
Sensirion sht2 = Sensirion(dataPin2, sclkPin2);

uint16_t rawData, rawData2;
float temperature, temperature2;
float mean;

void setup()
{
  Serial.begin(9600);
  delay(15);                           // Wait at least 11 ms before first cmd
  sht.measTemp(&rawData);              // Maps to: sht.meas(TEMP, &rawData, BLOCK)
  temperature = sht.calcTemp(rawData);
  sht2.measTemp(&rawData2);              // Maps to: sht.meas(TEMP, &rawData, BLOCK)
  temperature2 = sht2.calcTemp(rawData2);
}

void loop()
{
  sht.meas(TEMP, &rawData, NONBLOCK);
  if (sht.measRdy()) {                         // Process temperature measurement
    temperature = sht.calcTemp(rawData);
  }

  sht2.meas(TEMP, &rawData2, NONBLOCK);
  if (sht2.measRdy()) {                         // Process temperature measurement
    temperature2 = sht2.calcTemp(rawData2);
  }

  logData();
  delay(2000);
}

void logData() {
  Serial.print("Temperature 1 = ");   Serial.print(temperature);
  Serial.println(" C");
  Serial.print("Temperature 2 = ");   Serial.print(temperature2);
  Serial.println(" C");
  mean = (temperature + temperature2)/2;
  Serial.print("Mean Temperature = ");   Serial.print(mean);
  Serial.println(" C");
  Serial.println("*********************************");  
}
