import serial
import numpy as np
import cv2 as cv
import time
import readimage
import datetime



class Camera():
    def __init__(self):
        self.width = 176
        self.height = 144
        self.__arduino = serial.Serial('/dev/cu.usbmodem101', baudrate=9600, timeout=2)
        
    def read(self):
         # Send a command to tell Arduino to capture one frame
        self.__arduino.write(b"r")
        
        # Give Arduino a moment to capture and send
        # time.sleep(1)

        # We expect 176 * 144 * 2 bytes for RGB565
        bytes_to_read = self.width * self.height * 2

        # Read raw bytes
        data = self.__arduino.read(bytes_to_read)

        # Decode using your readimage.py logic (Format.RGB565)
        image_np = readimage.get_image(readimage.Format.RGB565, self.width, self.height, ser_data=data)
        
        return image_np

if __name__ == "__main__":
    cam = Camera()
    img = cam.read()

    cv.imshow("Camera View", img)
    cv.waitKey(0)
    cv.destroyAllWindows()
