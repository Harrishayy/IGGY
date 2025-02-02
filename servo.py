import time

class Servo():
    def __init__(self, servo_board:object, pin:int = 0, initial_pos:int=0) -> None:
        self.__servo_board = servo_board
        self.__pin = pin
        self.__position = initial_pos
        
        self.set_position(self.__position)

    def set_position(self, position:int=0) -> None:
        # move to position by communicating to arduino
        string = str(self.__pin) + "/" + str(position)
        self.__servo_board.write(bytes(string, encoding="utf-8"))
        
        time.sleep(0.01)
        # message = self.__servo_board.readline()
        # print("Message: ", message)
