import serial
import time

from leg import Leg

class Robot():
    def __init__(self) -> None:
        #self.arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
        self.servo_board = serial.Serial(port='COM3', baudrate=115200, timeout=1)

        self.leg_fl = Leg(self.servo_board, 2, 3, 4)
        self.leg_fr = Leg(self.servo_board, 5, 6, 7)
        self.leg_bl = Leg(self.servo_board, 8, 9, 10)
        self.leg_br = Leg(self.servo_board, 11, 12, 13)

            
    def run(self) -> None:  
        self.leg_fl.hip_z.set_position(90)
        time.sleep(1)
        self.leg_fl.hip_z.set_position(180)
        time.sleep(1)
        self.leg_fl.hip_z.set_position(0)
        time.sleep(1)
        
        self.leg_fl.hip_y.set_position(90)
        time.sleep(1)
        self.leg_fl.hip_y.set_position(180)
        time.sleep(1)
        self.leg_fl.hip_y.set_position(0)
        time.sleep(1)


if __name__ == "__main__":
    try:
        robot = Robot()
        robot.run()
        
    except Exception as error:
        print(f"Error:\n{error}")