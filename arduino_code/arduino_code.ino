
#include <Wire.h> //communicate with I2C devices
#include "DHT.h" //library for Digital Humidity Sensor


#define DHTPIN 6
#define DHTTYPE DHT11

#define LED_PIN 3


DHT dht(DHTPIN, DHTTYPE);



void fanVoltage(float temp)
{
  //use digital potentiometer to adjust voltage of H bridge ciruit
}

void setup() 
{
  Serial.begin(115200);
  dht.begin();

  pinMode(LED_PIN, OUTPUT);

  digitalWrite(LED_PIN, HIGH);


  Serial.println("");

  
}


void loop() {
  time = millis();

  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();

  fanVoltage(temp);

}