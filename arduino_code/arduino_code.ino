#include <Wire.h> //communicate with I2C devices
//#include "DHT.h" //library for Digital Humidity Sensor

#define DHTPIN 8
#define DHTTYPE DHT11

#define LED_PIN 2
#define Addr 0x53

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
  Wire.begin(); 
  // Initialise serial communication, set baud rate = 9600 
  Serial.begin(9600);   
  // Start I2C Transmission 
  Wire.beginTransmission(Addr); 
  // Select bandwidth rate register 
  Wire.write(0x2C); 
  // Normal mode, Output data rate = 100 Hz 
  Wire.write(0x0A); 
  // Stop I2C transmission 
  Wire.endTransmission();   
  // Start I2C Transmission 
  Wire.beginTransmission(Addr); 
  // Select power control register 
  Wire.write(0x2D); 
  // Auto-sleep disable 
  Wire.write(0x08); 
  // Stop I2C transmission 
  Wire.endTransmission();   
  // Start I2C Transmission 
  Wire.beginTransmission(Addr); 
  // Select data format register 
  Wire.write(0x31); 
  // Self test disabled, 4-wire interface, Full resolution, Range = +/-2g 
  Wire.write(0x08); 
  // Stop I2C transmission 
  Wire.endTransmission(); 
  delay(300);
 
  
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
    unsigned int data[6]; 
    for(int i = 0; i < 6; i++) 
    {   
    // Start I2C Transmission   
    Wire.beginTransmission(Addr);   
    // Select data register   
    Wire.write((50 + i));   
    // Stop I2C transmission   
    Wire.endTransmission();       
    // Request 1 byte of data   
    Wire.requestFrom(Addr, 1);       
    // Read 6 bytes of data   
    // xAccl lsb, xAccl msb, yAccl lsb, yAccl msb, zAccl lsb, zAccl msb   
    if(Wire.available() == 1)   
    {     
    data[i] = Wire.read();   
    } 
    }   
    // Convert the data to 10-bits 
    int xAccl = (((data[1] & 0x03) * 256) + data[0]); 
    if(xAccl > 511) 
    {   
    xAccl -= 1024; 
    } 
    int yAccl = (((data[3] & 0x03) * 256) + data[2]); 
    if(yAccl > 511) 
    {   
    yAccl -= 1024; 
    } 
    int zAccl = (((data[5] & 0x03) * 256) + data[4]); 
    if(zAccl > 511) 
    {   
    zAccl -= 1024; 
    }   
    // Output data to serial monitor 
    Serial.print("Acceleration in X-Axis is : "); 
    Serial.println(xAccl); 
    Serial.print("Acceleration in Y-Axis is : "); 
    Serial.println(yAccl); 
    Serial.print("Acceleration in Z-Axis is : "); 
    Serial.println(zAccl); 
    delay(300);
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


 