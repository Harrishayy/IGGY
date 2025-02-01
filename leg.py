from servo import Servo

class Leg():
    def __init__(self):
        self.knee = Servo()
        self.hip_y = Servo()
        self.hip_z = Servo()
        h