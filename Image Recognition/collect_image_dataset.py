import cv2 as cv
import numpy as np

from window_capture import WindowCapture
from util import generate_file_name

"""
Before use make sure there is a folder directory which looks something like this, with an Image Dataset folder with Positive and Negative folders:

Code Folder
    - Image_Dataset
        - Positive
            - img1.png
            - ...
        - Negative
            - img2.png
            - ...
    - collect_image_dataset.py
    - util.py
    - window_capture.py
"""

def dataset_screenshot_save(window_name=None):
    #Trying to capture specific window only but shows only a black screen
    if window_name is not None:
        window = WindowCapture()
        window_name = window.get_window_name(window_name) #returns the full window name to pass to the win32 api
        window_capture = WindowCapture(window_name)

    else:
        #no window input so it records the whole of your primary screen
        window_capture = WindowCapture()

    while True:
        img = window_capture.get_screenshot() #raw window image

        cv.imshow("Computer Vision", img)

        key_press = cv.waitKey(1) #waits a milisecond for key press in every loop

        if key_press == ord("q") or key_press == 27: #27 is escape key
            #exit program
            cv.destroyAllWindows()
            break

        elif key_press == ord("p"):
            #save screenshot to positive image folder
            file_name = generate_file_name()
            cv.imwrite(f"Image_Dataset/Positive/{file_name}", img)
            print(f"Image saved - Image_Dataset/Positive/{file_name}")

        elif key_press == ord("n"):
            #save screenshot to negative image folder
            file_name = generate_file_name()
            cv.imwrite(f"Image_Dataset/Negative/{file_name}", img)
            print(f"Image saved - Image_Dataset/Negative/{file_name}")
            
if __name__ == "__main__":
    dataset_screenshot_save()