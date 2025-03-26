#include <Wire.h> //communicate with I2C devices
#include <DHT.h> //library for Digital Humidity Sensor
#include <Motoron.h> //library for motoron motor driver

MotoronI2C md;

#define MOTOR_SPEED_1_PIN 5 //set pwm speed 0-255
#define MOTOR_SPEED_2_PIN 6 //set pwm speed 0-255
#define MOTOR_1_PIN 4 //set digital to alternate direction
#define MOTOR_2_PIN 7

#define DHTPIN 8
#define DHTTYPE DHT11

#define LED_PIN 2

#define ADXL345 0x53 // The ADXL345 sensor I2C address

#define FAN_PIN 9
#define MOTORON_ADDRESS 0x59

//fan control
float FAN_GAIN = 200.0;
int pwm = 0;

//ADXL345 variables
int16_t X_raw, Y_raw, Z_raw;
float X_out, Y_out, Z_out;
char x_str[10], y_str[10], z_str[10];

//DHT11 variables
float temp;
float humidity;

String data;
String output;
unsigned int acc_data[6]; 

int index = -1;
int motor_id = 0;
int speed = 0;
int id = -1;

//for LED blinking
bool led_state = true;
unsigned long loop_time = 0;
unsigned long initial_time = 0;
unsigned int led_interval = 500; //milliseconds


DHT dht(DHTPIN, DHTTYPE);

//set motor speed for fan
void setFanSpeed(uint8_t motor, int16_t speed) {
  md.setSpeed(1, speed);
}

//turn voltage to pwm
void fanVoltage(float temp)
{ 
  pwm = floor(FAN_GAIN * temp) - 4750;

  if (pwm > 3200){
    pwm = 3200;
  }
  else if (pwm < 0){
    pwm = 0;
  }

  if (temp <= 26){
    pwm = 0;
  }

  // Serial.print("Temperature: ");
  // Serial.println(temp);

  // Serial.print("Fan PWM: ");
  // Serial.println(pwm);

  // analogWrite(FAN_PIN, 255);
  setFanSpeed(1, pwm);
}

void set_motor(int motor_id, int speed)
{

  Serial.print("Motor ID: ");
  Serial.println(motor_id);
  Serial.print("Motor speed: ");
  Serial.println(speed);

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
        Serial.print("Speed: ");
        Serial.println(speed);
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
  pinMode(FAN_PIN, OUTPUT);

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
  Wire.write(0x2C); 
  // Normal mode, Output data rate = 100 Hz 
  Wire.write(0x0A); 
  // Stop I2C transmission 
  Wire.endTransmission();   
  // Start I2C Transmission 
  Wire.beginTransmission(ADXL345); 
  // Select power control register 
  Wire.write(0x2D); 
  // Auto-sleep disable 
  Wire.write(0x08); 
  // Stop I2C transmission 
  Wire.endTransmission();   
  // Start I2C Transmission 
  Wire.beginTransmission(ADXL345); 
  // Select data format register 69
  Wire.write(0x31); 
  // Self test disabled, 4-wire interface, Full resolution, Range = +/-2g 
  Wire.write(0x08); 
  // Stop I2C transmission 
  Wire.endTransmission();

  delay(100);
  
  Serial.println("Initialising DHT11...");
  dht.begin();
  Serial.println("DHT11 Connected!");

  Serial.println("Initialising Motoron Motor Driver...");

  md.reinitialize();    // Bytes: 0x96 0x74
  md.disableCrc();      // Bytes: 0x8B 0x04 0x7B 0x43
  md.clearResetFlag();

  Serial.println("Motoron Motor Driver Connected!");

  delay(100);
}


void loop() {
  id = -1;

  if (Serial.available()){
    //data in format "pin/position"
    data = Serial.readString();
    Serial.flush();

    //find index of split between motor id and speed
    index = data.indexOf('/');
    
    if (index > -1){
      id = data.substring(0, index).toInt();
    }
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
    
    for(int i = 0; i < 6; i++) 
    {   
      // Start I2C Transmission   
      Wire.beginTransmission(ADXL345);   
      // Select data register   
      Wire.write((50 + i));   
      // Stop I2C transmission   
      Wire.endTransmission();       
      // Request 1 byte of data   
      Wire.requestFrom(ADXL345, 1);       
      // Read 6 bytes of data   
      // xAccl lsb, xAccl msb, yAccl lsb, yAccl msb, zAccl lsb, zAccl msb   
      if(Wire.available() == 1)   
      {     
        acc_data[i] = Wire.read();   
      } 
    }   
    // Convert the data to 10-bits 
    X_raw = (((acc_data[1] & 0x03) * 256) + acc_data[0]); 
    if(X_raw > 511) 
    {   
      X_raw -= 1024; 
    } 

    Y_raw = (((acc_data[3] & 0x03) * 256) + acc_data[2]); 
    if(Y_raw > 511) 
    {   
      Y_raw -= 1024; 
    } 

    Z_raw = (((acc_data[5] & 0x03) * 256) + acc_data[4]); 
    if(Z_raw > 511) 
    {   
      Z_raw -= 1024; 
    }
    
    X_out = X_raw * 0.0039 * 9.81;
    Y_out = Y_raw * 0.0039 * 9.81;
    Z_out = Z_raw * 0.0039 * 9.81;
    
    // Output data to serial monitor 
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
    }
    else
    {
      digitalWrite(LED_PIN, HIGH);
      led_state = true;
    }

    //fan control in loop as only really needs to be checked every second, so using same loop to reduce memory requirements of an additional checking loop for DHT11
    temp = dht.readTemperature();
    humidity = dht.readHumidity();

    

    fanVoltage(temp);
  }

  

}


 