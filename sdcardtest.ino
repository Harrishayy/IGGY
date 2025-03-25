#include<TFT_eSPI.h>
#include<SPI.h>
#include<TouchScreen.h>
#include <SD.h>

TFT_eSPI tft = TFT_eSPI();       // invoke custom library

#define Y_plus A1
#define X_plus A2
#define Y_minus A3
#define X_minus A4

#define TS_YMIN 110
#define TS_XMIN 200
#define TS_YMAX 870
#define TS_XMAX 880

#define SD_CS  4
#define LCD_CS 5
#define DC     9
#define RST    8

TouchScreen ts = TouchScreen(X_plus, Y_plus, X_minus, Y_minus, 300);
File image;

void drawBmp(const char *filename, int16_t x, int16_t y);
void listFiles();
int emotion = 1;
int emotion_prev = 1;
int tired = 0;

void setup() {
  // put your setup code here, to run once:
  tft.init();
  tft.setRotation(3);   // for orientation
  Serial.begin(115200); // For debug
  tft.fillScreen(TFT_BROWN);
  Serial.println("sd card test initiated");
  pinMode(A1, INPUT); // Y+
  pinMode(A2, INPUT); // X+
  pinMode(A3, INPUT); // Y-
  pinMode(A4, INPUT); // X-

  pinMode(0, INPUT);  // receive pin?

  Serial.println("initialising SD card read...");
  if (!SD.begin(SD_CS)) {
    Serial.println("failed noooo");
    return;
  }
  Serial.println("OK!!! SD card read");

  tft.fillScreen(TFT_WHITE);

  listFiles();

  drawBmp("HAPPY.BMP", 0, 0);    // draw default face (happy?)

  Serial.println("entering loop");
}

void loop() {   // calibration
  // get serial input
  if (Serial.available()) {
    emotion = Serial.read();
  }

  TSPoint p = ts.getPoint();
  if (p.z > 0 && p.z < 10000) {     // check if a touch is registered
    // change emotion
    Serial.print("pressure: ");

    int x = map(p.x, TS_XMIN, TS_XMAX, 0, 240);
    int y = map(p.y, TS_YMIN, TS_YMAX, 0, 320);
    Serial.println(p.z);

    if (p.z < 400)  {
      emotion = 4;
    }
    else {
      emotion = 1;
    }
  }

  if (emotion == emotion_prev)  {
    tired++;
    // Serial.println(tired);
    if (tired > 10000)  {
      drawBmp("SLEEPY.BMP", 0, 0);
      emotion = 3;
      emotion_prev = emotion;
      tired = 0;
    }    
  }
  else  {

    switch(emotion) {
      case 1:   // happy
        drawBmp("HAPPY.BMP", 0, 0);
        emotion_prev = emotion;
        break;

      case 2:   // sad
        drawBmp("SAD.BMP", 0, 0);
        emotion_prev = emotion;
        break;

      case 3:   // sleepy
        drawBmp("SLEEPY.BMP", 0, 0);
        emotion_prev = emotion;
        break;

      case 4:   // angry
        drawBmp("ANGRY.BMP", 0, 0);
        emotion_prev = emotion;
        break;

      default:
        break;

    }
  }

  delay(5);

}

void drawBmp(const char *filename, int16_t x, int16_t y) {
  File bmpFile;
  bmpFile = SD.open(filename);

  if (!bmpFile) {
    Serial.println("BMP file not found!??");
    return;
  }

  uint8_t header[54];  // BMP Header is 54 bytes
  bmpFile.read(header, 54);  // Read the header

  uint32_t w = header[18] | (header[19] << 8) | (header[20] << 16) | (header[21] << 24);
  uint32_t h = header[22] | (header[23] << 8) | (header[24] << 16) | (header[25] << 24);

  Serial.print("BMP Width: "); Serial.println(w);
  Serial.print("BMP Height: "); Serial.println(h);

  uint16_t bitDepth = header[28] | (header[29] << 8);
  if (bitDepth != 24) {
    Serial.println("Unsupported BMP format!");
    bmpFile.close();
    return;
  }

  // Read and convert pixel data one row at a time to avoid memory overflow
  bmpFile.seek(54);  // Skip the header

  uint8_t row[3 * w];  // Temporary row buffer (24-bit RGB for one row)

  // Loop through the rows and read pixels one by one
  for (int rowIdx = 0; rowIdx < h; rowIdx++) {
    // Read one row of pixels (24 bits per pixel)
    bmpFile.read(row, 3 * w);

    // Convert each pixel and send to TFT
    for (int colIdx = 0; colIdx < w; colIdx++) {
      uint8_t b = row[3 * colIdx];      // Blue component
      uint8_t g = row[3 * colIdx + 1];  // Green component
      uint8_t r = row[3 * colIdx + 2];  // Red component

      // Convert 24-bit RGB to 16-bit RGB565
      uint16_t color = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3);
      
      // Write pixel to TFT
      tft.drawPixel(320 - (x + colIdx), y + rowIdx, color);
    }
  }

  bmpFile.close();
}

void listFiles() {
  File root = SD.open("/");
  while (true) {
    File entry = root.openNextFile();
    if (!entry) {
      break;
    }
    Serial.print("File found: ");
    Serial.println(entry.name());
    entry.close();
  }
}