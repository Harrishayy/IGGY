import serial
import time
import cv2

from leg import Leg
from motor import MotorBoard, Motor

class Robot():
    def __init__(self, debug:bool=False) -> None:
        if debug:
            self.camera = cv2.VideoCapture(0)
        else:
            self.arduino = serial.Serial(port='COM4', baudrate=9600, timeout=1)
            #self.servo_board = serial.Serial(port='COM3', baudrate=115200, timeout=1)
            self.motor_board = MotorBoard(self.arduino)

        

        #self.leg_fl = Leg(self.servo_board, 2, 3, 4)
        #self.leg_fr = Leg(self.servo_board, 5, 6, 7)
        #self.leg_bl = Leg(self.servo_board, 8, 9, 10)
        #self.leg_br = Leg(self.servo_board, 11, 12, 13)

            
    def run(self) -> None:  
        self.motor_board.forward(100)
        time.sleep(1)
        self.motor_board.stop()


if __name__ == "__main__":
    try:
        robot = Robot()
        robot.run()
        
    except Exception as error:
        print(f"Error:\n{error}")