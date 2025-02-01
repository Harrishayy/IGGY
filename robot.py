from leg import Leg

class Robot():
    def __init__(self) -> None:
        fl_leg = Leg()
        fr_leg = Leg()
        bl_leg = Leg()
        br_leg = Leg()

            
    def run(self) -> None:
        pass


if __name__ == "__main__":
    try:
        robot = Robot()
        robot.run()
    except Exception as error:
        print(f"Error:\n{error}")