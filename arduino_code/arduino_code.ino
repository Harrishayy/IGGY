
#include <Wire.h> //communicate with I2C devices
//#include "DHT.h" //library for Digital Humidity Sensor


#define DHTPIN 8
#define DHTTYPE DHT11

#define LED_PIN 2

String data;
int index = -1;
int motor_id = 0;
int speed = 0;

//for LED blinking
bool led_state = true;
unsigned long loop_time = 0;
unsigned long initial_time = 0;
unsigned int led_interval = 500; //milliseconds

#define MOTOR_SPEED_1_PIN 6 //set pwm speed 0-255
#define MOTOR_SPEED_2_PIN 5 //set pwm speed 0-255
#define MOTOR_1_PIN 7 //set digital to alternate direction
#define MOTOR_2_PIN 4

//DHT dht(DHTPIN, DHTTYPE);


void fanVoltage(float temp)
{
  //use digital potentiometer to adjust voltage of H bridge ciruit
}

void setup() 
{
  Serial.begin(115200);
  Serial.setTimeout(1); 

  pinMode(LED_PIN, OUTPUT);

  pinMode(MOTOR_1_PIN, OUTPUT);
  pinMode(MOTOR_2_PIN, OUTPUT);
  pinMode(MOTOR_SPEED_1_PIN, OUTPUT);
  pinMode(MOTOR_SPEED_2_PIN, OUTPUT);
  
  //dht.begin();
  
}


void loop() {
  //continuous loop waiting until connection is made
  while (!Serial.available());


  //data in format "pin/position"
  data = Serial.readString();

  //find index of split between motor id and speed
  index = data.indexOf('/');


  if (index > -1)
  {
    motor_id = data.substring(0, index).toInt();
    speed = data.substring(index + 1).toInt();
    String strnum = String(speed);
    //Serial.print(motor_id);

    switch(motor_id)
    {
      case 0:
        if (speed > 0)
        {
          //Serial.println(speed);
          analogWrite(MOTOR_SPEED_1_PIN, speed);
          digitalWrite(MOTOR_1_PIN, HIGH);
        }

        else if (speed < 0)
        {
          speed = -speed;
          //Serial.println(speed);
          analogWrite(MOTOR_SPEED_1_PIN, speed);
          digitalWrite(MOTOR_1_PIN, LOW);
        }

        else
        {
          //Serial.println(0);
          analogWrite(MOTOR_SPEED_1_PIN, 0);
          digitalWrite(MOTOR_1_PIN, LOW);
        }
      
      
        break;

      case 1:
        if (speed > 0)
        {
          //Serial.println(speed);
          analogWrite(MOTOR_SPEED_2_PIN, speed);
          digitalWrite(MOTOR_2_PIN, HIGH);
        }

        else if (speed < 0)
        {
          speed = -speed;
          //Serial.println(speed);
          analogWrite(MOTOR_SPEED_2_PIN, speed);
          digitalWrite(MOTOR_2_PIN, LOW);
        }

        else
        {
          //Serial.println(0);
          analogWrite(MOTOR_SPEED_2_PIN, 0);
          digitalWrite(MOTOR_2_PIN, LOW);
        }
      
        break;
    }

  }


  loop_time = millis();

  if (loop_time - initial_time > led_interval)
  {
    initial_time = millis();

    if (led_state)
    {
      digitalWrite(LED_PIN, LOW);
      led_state = false;
      //Serial.println("Off");
    }
    else
    {
      digitalWrite(LED_PIN, HIGH);
      led_state = true;
      //Serial.println("On");
    }
  }

  //float temp = dht.readTemperature();
  //float humidity = dht.readHumidity();

  //fanVoltage(temp);

}