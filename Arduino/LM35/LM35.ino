int pinLara = A0, pinExternal = A1;
double tempLara = 0, tempExternal = 0;
double tempLaraAmostra = 0, tempExternalAmostra = 0;
int i = 0;

void setup()
{
  Serial.begin(9600);  
  pinMode(pinLara, INPUT);
  pinMode(pinExternal, INPUT);
}

void loop()
{
  for(i = 0;i<=7;i++){ // Loop que faz a leitura da temperatura 8 vezes
    tempExternalAmostra = analogRead(pinExternal);
    tempLaraAmostra = analogRead(pinLara); 
    
    tempExternal = tempExternalAmostra + tempExternal;
    tempLara = tempLaraAmostra + tempLara;
    
    delay(10);
  } 

  tempExternal = tempExternal/8.0;
  tempLara = tempLara/8.0;
  
  Serial.print("TL:");  Serial.print(tempLara,2);
  Serial.print("|TE:");  Serial.print(tempExternal,2);
  Serial.println();
  
  tempExternal = 0;
  tempLara = 0;
  delay(5000);
}  
