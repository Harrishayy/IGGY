import time

TIME_DELAY = 0.008

class MotorBoard():
    def __init__(self, arduino:object):
        self.motor_l = Motor(arduino, 0)
        self.motor_r = Motor(arduino, 1)

    def forward(self, speed:int):
        self.motor_l.set_speed(speed)
        time.sleep(TIME_DELAY)
        self.motor_r.set_speed(speed)

    def backward(self, speed:int):
        self.motor_l.set_speed(-speed)
        time.sleep(TIME_DELAY)
        self.motor_r.set_speed(-speed)

    def left(self, speed:int):
        self.motor_l.set_speed(speed)
        time.sleep(TIME_DELAY)
        self.motor_r.set_speed(-speed)

    def right(self, speed:int):
        self.motor_l.set_speed(-speed)
        time.sleep(TIME_DELAY)
        self.motor_r.set_speed(speed)

    def stop(self):
        self.motor_l.set_speed(0)
        time.sleep(TIME_DELAY)
        self.motor_r.set_speed(0)

    


class Motor():
    def __init__(self, arduino:object, id:int = 0) -> None:
        self.__arduino = arduino
        self.__id = id
        # ID 0 for left, 1 for right
        

    def set_speed(self, speed:int=0) -> None:
        """
        Set the speed of the motor.
        """

        # move to position by communicating to arduino
        string = str(self.__id) + "/" + str(speed)
        self.__arduino.write(bytes(string, encoding="utf-8"))

        #message = self.__arduino.readline()
        #print("Message: ", message)


    def percentage_to_pwm(self, value:int):
        """
        Input percentage speed 0-100%, and returns value range for pwm
        """
        #max 255
        #stop 0
        #max reverse 1
        pwm = value * 1.28 + 127

        return pwm
