import serial
import numpy as np
import cv2 as cv

class Camera():
    def __init__(self):
        self.width = 176
        self.height = 144
        self.__arduino = serial.Serial(port='COM8', baudrate=1000000, timeout=1)
    
    def read(self):
        self.__arduino.write(b"r")

        #receive the image data
        message = self.__arduino.read(self.width * self.height * 2)  #read number of raw bytes of pixels

        #check if the expected amount of data was received
        if len(message) != self.width * self.height * 2:
            print(f"Incomplete data received: {len(message)} bytes.")
            return
        
        rgb565_data = np.frombuffer(message, dtype=np.uint16)

        #convert RGB565 to RGB888
        rgb888_data = self.rgb565_to_rgb888(rgb565_data)

        rgb_image = rgb888_data.reshape((self.height, self.width, 3))

        return rgb_image

    def rgb565_to_rgb888(self, rgb565_data):
        r = ((rgb565_data >> 11) & 0x1F) * 255 // 31
        g = ((rgb565_data >> 5) & 0x3F) * 255 // 63
        b = (rgb565_data & 0x1F) * 255 // 31

        #stack RGB channels together in the form RGB
        return np.stack((r, g, b), axis=-1).astype(np.uint8)


if __name__ == "__main__":
    cam = Camera()
    img = cam.read()

    cv.imshow("Camera View", img)
    cv.waitKey(0)
    cv.destroyAllWindows()
