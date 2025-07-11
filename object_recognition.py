import cv2
import matplotlib as plt

DETECTION_COLOUR = (0,0,255)
DETECTION_THICKNESS = 2

#Distance to object(mm) = focal length(mm) x real height(mm) x image height(px) / object height(pixels) x sensor height(mm)

#Camera settings for OV7675
CAMERA_WIDTH = 640 #px
CAMERA_HEIGHT = 480 #px
FOCAL_LENGTH = 1.75 #mm
CAMERA_SENSOR_HEIGHT = 3.58 #mm
ROBOT_ESTIMATED_HEIGHT = 65 #mm

# distance_to_robot = (FOCAL_LENGTH * ROBOT_ESTIMATED_HEIGHT * CAMERA_HEIGHT) / (height * CAMERA_SENSOR_HEIGHT)
# distance becomes (CAMERA_CONSTANT / height) of robot in px
CAMERA_CONSTANT = (FOCAL_LENGTH * ROBOT_ESTIMATED_HEIGHT * CAMERA_HEIGHT) /  CAMERA_SENSOR_HEIGHT
#depends on focal length of camera, need to edit based on camera we are given

# link to haar cascades for human body: https://github.com/opencv/opencv/tree/master/data/haarcascades

def detect_object(img_data) -> list:
    """
    Returns an array of tuples for the data of detected robots which are (x,y,width,height) x,y = 0 at top left of screen, width and height to the right and down.
    """

    img_gray = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
    
    #the trained data for detection
    #tutorial for use in https://medium.com/@vipulgote4/guide-to-make-custom-haar-cascade-xml-file-for-object-detection-with-opencv-6932e22c3f0e
    robot_detection_data = cv2.CascadeClassifier("cascade.xml")
    
    found = robot_detection_data.detectMultiScale(img_gray, minNeighbors=10, minSize=(20, 20))
    
    return found


def draw_detection(img, found:list) -> None:
    """
    Draws detection boundary on image with objects outlined in found. found is list of [[x,y,width,height], ...]
    """
    
    amount_found = len(found)

    if amount_found != 0:
        for (x, y, width, height) in found:
            # draw a green rectangle around every detected object
            cv2.rectangle(img, (x, y), (x + height, y + width), DETECTION_COLOUR, DETECTION_THICKNESS)

    return img



def calculate_distance(height:float) -> float:
    """
    Calculates the approximate distance to the object given the height in pixels of the object in the image.
    """
    
    distance_to_robot = CAMERA_CONSTANT / height #distance in mm
    
    return distance_to_robot