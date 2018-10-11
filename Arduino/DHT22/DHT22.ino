// Programa : Sensor de temperatura DHT22
// Autor : Arduino e Cia

#include <DHT.h>
#include <LiquidCrystal.h>

// Pino conectado ao pino de dados do sensor
#define DHTPIN 7

// Pinos do display
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

// Utilize a linha de acordo com o modelo do sensor
//#define DHTTYPE DHT11   // Sensor DHT11
#define DHTTYPE DHT22   // Sensor DHT 22  (AM2302)
//#define DHTTYPE DHT21   // Sensor DHT 21 (AM2301)

// Definicoes do sensor : pino, tipo
DHT dht(DHTPIN, DHTTYPE);

// Array simbolo grau
byte grau[8] ={ B00001100, 
                B00010010, 
                B00010010, 
                B00001100, 
                B00000000, 
                B00000000, 
                B00000000, 
                B00000000,}; 
                
void setup() {
  // put your setup code here, to run once:
  // Inicializa o display
  lcd.begin(16, 2);
  lcd.clear();
  // Cria o caracter customizado com o simbolo do grau
  lcd.createChar(0, grau); 
  // Informacoes iniciais no display
  lcd.setCursor(0,0);
  lcd.print("Temp. : ");
  lcd.setCursor(13,0);
  // Mostra o simbolo do grau
  lcd.write(byte(0));
  lcd.print("C");
  lcd.setCursor(0,1);
  lcd.print("Umid. : ");
  lcd.setCursor(14,1);
  lcd.print("%");

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
  lcd.setCursor(8,0);
  lcd.print(t);
  Serial.print(" *C  ");
  // Mostra a umidade no serial monitor e no display
  Serial.print("Umidade : "); 
  Serial.print(h);
  Serial.println(" %");
  lcd.setCursor(8,1);
  lcd.print(h);
}
