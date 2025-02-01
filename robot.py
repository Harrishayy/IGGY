import serial

from leg import Leg

class Robot():
    def __init__(self) -> None:
        arduino = serial.Serial(port='COM3', baudrate=115200, timeout=1)

        leg_fl = Leg()
        leg_fr = Leg()
        leg_bl = Leg()
        leg_br = Leg()

            
    def run(self) -> None:
        pass


if __name__ == "__main__":
    try:
        robot = Robot()
        robot.run()
    except Exception as error:
        print(f"Error:\n{error}")