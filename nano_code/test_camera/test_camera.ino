/*
  Active Learning Labs
  Harvard University 
  tinyMLx - OV7675 Camera Test

*/

#include <TinyMLShield.h>

bool commandRecv = false; // flag used for indicating receipt of commands from serial port
bool liveFlag = false; // flag as true to live stream raw camera bytes, set as false to take single images on command
bool captureFlag = false;

// Image buffer;
byte image[176 * 144 * 2]; // QCIF: 176x144 x 2 bytes per pixel (RGB565)
int bytesPerFrame;
String data;

void setup() {
  Serial.begin(1000000);
  while (!Serial);

  initializeShield();

  // Initialize the OV7675 camera
  if (!Camera.begin(QCIF, RGB565, 1, OV7675)) {
    Serial.println("Failed to initialize camera");
    while (1);
  }
  bytesPerFrame = Camera.width() * Camera.height() * Camera.bytesPerPixel();
}

void loop() {
  // Read incoming commands from serial monitor
  while (Serial.available()) {
    data = Serial.readString();

    if (data == "r") 
    {
      Camera.readFrame(image);
      delay(100); //delay to make sure full frame is read

      for (int i = 0; i < bytesPerFrame; i += 2) {
        Serial.print("0x");
        Serial.print(image[i+1], HEX);
        Serial.print(image[i], HEX);

        if (i != bytesPerFrame - 2) {
          Serial.print(",");
        }
      }

      Serial.println();
    } 

  // if (captureFlag) {
  //   captureFlag = false;
  //   Camera.readFrame(image);
  //   for (int i = 0; i < bytesPerFrame - 1; i += 2) {
  //     Serial.print("0x");
  //     Serial.print(image[i+1], HEX);
  //     Serial.print(image[i], HEX);
  //     if (i != bytesPerFrame - 2) {
  //       Serial.print(", ");
  //     }
  //   }
  //   Serial.println();
  // }
  }
}