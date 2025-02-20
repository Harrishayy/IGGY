#include <Arduino_OV767X.h>

unsigned short pixels[640 * 480]; // QCIF: 176x144 X 2 bytes per pixel (RGB565)

void camInit(void){
  writeReg(0x12, 0x80);
  _delay_ms(100);
  wrSensorRegs8_8(ov7675_default_regs);
  writeReg(REG_COM10, 32);//PCLK does not toggle on HBLANK.
}

void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}
