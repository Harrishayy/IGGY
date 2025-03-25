import serial
import numpy as np
import cv2 as cv


emotions_dict = {'happy':1,"sad":2,"sleepy":3,"sleepy":4}

class Face():
    def __init__(self):
        self.__arduino = serial.Serial('/dev/cu.weeeeee', baudrate=115200, timeout=2)
        self.emotion_meter = 1
    def read(self, state):
        self.state = emotions_dict[state]
        #define variable...
        string = str(self.__id) + "/" + str(self.state)
        self.__arduino.write(bytes(string, encoding="utf-8"))
        
