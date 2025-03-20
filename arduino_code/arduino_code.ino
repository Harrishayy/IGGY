
#include <Wire.h> //communicate with I2C devices
//#include "DHT.h" //library for Digital Humidity Sensor

#define DHTPIN 8
#define DHTTYPE DHT11

#define LED_PIN 2

#define ADXL345 0x53 // The ADXL345 sensor I2C address

int16_t X_raw, Y_raw, Z_raw;
float X_out, Y_out, Z_out;
char x_str[10], y_str[10], z_str[10];

String data;
String output;
int index = -1;
int motor_id = 0;
int speed = 0;
int id = -1;

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

void set_motor(int motor_id, int speed)
{
  switch(motor_id)
  {
    case 0:
      if (speed > 0)
      {
        analogWrite(MOTOR_SPEED_1_PIN, speed);
        digitalWrite(MOTOR_1_PIN, HIGH);
      }

      else if (speed < 0)
      {
        speed = -speed;
        analogWrite(MOTOR_SPEED_1_PIN, speed);
        digitalWrite(MOTOR_1_PIN, LOW);
      }

      else
      {
        analogWrite(MOTOR_SPEED_1_PIN, 0);
        digitalWrite(MOTOR_1_PIN, LOW);
      }
    
      break;

    case 1:
      if (speed > 0)
      {
        analogWrite(MOTOR_SPEED_2_PIN, speed);
        digitalWrite(MOTOR_2_PIN, HIGH);
      }

      else if (speed < 0)
      {
        speed = -speed;
        analogWrite(MOTOR_SPEED_2_PIN, speed);
        digitalWrite(MOTOR_2_PIN, LOW);
      }

      else
      {
        analogWrite(MOTOR_SPEED_2_PIN, 0);
        digitalWrite(MOTOR_2_PIN, LOW);
      }
    
      break;
  }
}

void setup() 
{
  Serial.begin(500000);
  Serial.setTimeout(1); 

  pinMode(LED_PIN, OUTPUT);

  pinMode(MOTOR_1_PIN, OUTPUT);
  pinMode(MOTOR_2_PIN, OUTPUT);
  pinMode(MOTOR_SPEED_1_PIN, OUTPUT);
  pinMode(MOTOR_SPEED_2_PIN, OUTPUT);

  Serial.println("Initializing ADXL345...");
  Wire.begin();

  while (true) {
    Wire.beginTransmission(ADXL345);
    if (Wire.endTransmission() == 0) {
      break;
    }
    Serial.println("ADXL345 NOT FOUND! Retrying...");
    delay(1000); // Retry every second
  }

  Serial.println("ADXL345 Connected!");

  // Set ADXL345 to measuring mode
  Wire.beginTransmission(ADXL345);
  Wire.write(0x2D);
  Wire.write(8);  // Enable measurement
  Wire.endTransmission();

  delay(10);
  
}


void loop() {
  //continuous loop waiting until connection is made
  while (!Serial.available());

  //data in format "pin/position"
  data = Serial.readString();

  //find index of split between motor id and speed
  index = data.indexOf('/');
  
  if (index > -1){
    id = data.substring(0, index).toInt();
  }
  else{
    id = -1;
  }

  //calling to set motor
  if (id == 0 || id == 1)
  {
    speed = data.substring(index + 1).toInt();

    set_motor(id, speed);
  }

  //fetch accelerometer data
  if (id == 2)
  {
    Wire.beginTransmission(ADXL345);
    Wire.write(0x32); // Start with register 0x32 (ACCEL_XOUT_H)
    Wire.endTransmission(false);

    Wire.requestFrom(ADXL345, 6, true); // Read 6 registers total, each axis value is stored in 2 registers

    X_out = ( Wire.read()| Wire.read() << 8); // X-axis value

    X_out = X_out/256; //For a range of +-2g, we need to divide the raw values by 256, according to the datasheet

    Y_out = ( Wire.read()| Wire.read() << 8); // Y-axis value

    Y_out = Y_out/256;

    Z_out = ( Wire.read()| Wire.read() << 8); // Z-axis value

    Z_out = Z_out/256;

    // Serial.println(X_out);
    // Serial.println(Y_out);
    // Serial.println(Z_out);

    dtostrf(X_out, 4, 2, x_str);
    dtostrf(Y_out, 4, 2, y_str);
    dtostrf(Z_out, 4, 2, z_str);

    output = String(x_str) + "/" + String(y_str) + "/" + String(z_str);

    Serial.println(output);
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