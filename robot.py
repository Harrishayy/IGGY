import serial
import time
import cv2

from leg import Leg
from motor import MotorBoard, Motor
from camera import Camera
from emotions import Face
from object_recognition import detect_object, calculate_distance

DEAD_ZONE = 2
MAX_ACC = 1

DECREMENT_VAL = 1

class Robot():
    def __init__(self, debug:bool=False) -> None:
        self.__debug = debug
        self.camera = Camera()
        self.emote = Face()

    def initialise(self) -> None:
        if self.__debug:
            self.camera = cv2.VideoCapture(0)
        else:
            pass
            #self.arduino = serial.Serial(port="COM5", baudrate=500000, timeout=1)
            #self.motor_board = MotorBoard(self.arduino)

        #time.sleep(1) #give time for arduino to setup

    def shutdown(self) -> None:
        if not self.__debug:
            #self.arduino.close()
            pass
    def emotions(self) -> None:
        #happy
        if (150 >= self.emotion_meter > 100):
            self.emote.state = 1
        #sad
        elif(100 >= self.emotion_meter > 50):
            self.emote.state = 2
        #sleepy
        elif(50 > self.emotion_meter >= 0):
            self.emote.state = 3
        #angry
        elif(self.emotion_meter == 200):
            self.emote.state = 4
        #error handling
        else:
            self.emote.state = 3
        

    def autonomous(self) -> None:
        following = True
        Kp = 5

        left_speed = 0
        right_speed = 0

        while following:
            target = self.find_target()

            if target is None:
                continue

            pos = (target[0] + target[2]) / 2

            #pos if need to turn right, neg if need to turn left
            turn_error = pos - self.camera.width / 2

            #turn if need to then redetect the ball position
            if abs(turn_error) > DEAD_ZONE:
                right_speed -= Kp * turn_error
                left_speed += Kp * turn_error

                continue

            else:
                left_speed = right_speed

            ax, ay, az = self.read_accelerometer()

            if (ax > MAX_ACC):
                left_speed -= 5
                right_speed -= 5
            
            else:
                left_speed += 10
                right_speed += 10

        
    def find_target(self) -> tuple:
        """
        Uses the camera to locate the closest tennis ball and returns the target as a tuple of (x,y,width,height). Returns None if can not detect a ball.
        """
        img = self.camera.read()

        detected_balls = detect_object(img)

        if len(detected_balls) < 1:
            return None

        idx = 0
        min_dist = 0

        for i in range(len(detected_balls)-1):
            height = detected_balls[i][3]
            distance = calculate_distance(height)

            if distance < min_dist:
                min_dist = distance
                idx = i

        target = detected_balls[idx]

        return target


    def read_accelerometer(self) -> tuple:
        string = "2/"
        self.arduino.write(bytes(string, encoding="utf-8"))

        message = self.arduino.readline()

        try:
            data = message.decode("utf-8").strip()  # Decode safely
        except UnicodeDecodeError:
            print("Error: Received non-UTF-8 data")
            return None  # Ignore bad data

        if len(data) > 0:
            t = data.split("/")

            if len(t) != 3:
                return None
            
            x,y,z = float(t[0]), float(t[1]), float(t[2])

            return (x, y, z)
        
        return None
        
            
    def run(self) -> None:
        #test motor driver
        # self.motor_board.forward(255)
        # time.sleep(0.5)
        # self.motor_board.stop()
        # time.sleep(0.5)
        # self.motor_board.backward(255)
        # time.sleep(1)
        # self.motor_board.forward(0)
        if(self.emote.state != 200):
            self.emote.emotion_meter -= self.emote.emotion_meter
        
        
            
        #test acc
        # while True:
        #     self.read_accelerometer()
        #     time.sleep(1)

        




if __name__ == "__main__":
    try:
        robot = Robot(debug=False)
        robot.initialise()
        robot.run()
        robot.shutdown()
        
    except Exception as error:
        print(f"Error:\n{error}")