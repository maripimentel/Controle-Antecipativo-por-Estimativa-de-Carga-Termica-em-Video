#include <DHT_U.h>
#include <DHT.h>

#include <Adafruit_Sensor.h>

// Programa : Sensor de temperatura DHT22
// Autor : Arduino e Cia


// Pino conectado ao pino de dados do sensor
#define DHTPIN 8

// Utilize a linha de acordo com o modelo do sensor
//#define DHTTYPE DHT11   // Sensor DHT11
#define DHTTYPE DHT22   // Sensor DHT 22  (AM2302)
//#define DHTTYPE DHT21   // Sensor DHT 21 (AM2301)

// Definicoes do sensor : pino, tipo
DHT dht(DHTPIN, DHTTYPE);
                
void setup() {
  Serial.begin(9600); 
  Serial.println("Aguardando dados...");
  // Iniclaiza o sensor DHT
  dht.begin();
  
}

void loop() {
 // Aguarda 2 segundos entre as medicoes
  delay(2000);
  
  // Leitura da umidade
  float h = dht.readHumidity();
  // Leitura da temperatura (Celsius)
  float t = dht.readTemperature();

  // Mostra a temperatura no serial monitor e no display
  Serial.print("Temperatura: "); 
  Serial.print(t);
  Serial.print(" *C  ");
  // Mostra a umidade no serial monitor e no display
  Serial.print("Umidade : "); 
  Serial.print(h);
  Serial.println(" %");
}
