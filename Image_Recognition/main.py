import cv2 as cv
import numpy as np

import time

from window_capture import WindowCapture
from robot_recognition import detect_robot, draw_detection, show_distances


window_name = WindowCapture.get_window_name()
window_capture = WindowCapture(window_name)

loop_time = time.time()
while (True):
    screenshot = window_capture.get_screenshot() #raw window image

    found_robots = detect_robot(screenshot)
    img = draw_detection(screenshot, found_robots) #draws an outline of the robots
    img = show_distances(img, found_robots) #shows the distance to the robots

    cv.imshow("Computer Vision", img)

    # debug the loop rate
    print("FPS {}".format(1 / (time.time() - loop_time)))
    loop_time = time.time()

    key_press = cv.waitKey(1) #waits a milisecond for key press in every loop

    if key_press == ord("q") or key_press == 27:
        #exit program
        cv.destroyAllWindows()
        break


