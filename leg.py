from servo import Servo

class Leg():
    def __init__(self, servo_board:object, hip_z_pin:int=0, hip_y_pin:int=0, knee_pin:int=0,):
        self.knee = Servo(servo_board, knee_pin, 0)
        self.hip_y = Servo(servo_board, hip_y_pin, 0)
        self.hip_z = Servo(servo_board, hip_z_pin, 0)