import cv2
import matplotlib as plt

DETECTION_COLOUR = (0,0,255)
DETECTION_THICKNESS = 2
FPS = 24


def detect_object(img_data) -> list:
    """
    Returns an array of tuples for the data of detected robots which are (x,y,width,height) x,y = 0 at top left of screen, width and height to the right and down.
    """

    img_gray = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
    
    #the trained data for detection
    #tutorial for use in https://medium.com/@vipulgote4/guide-to-make-custom-haar-cascade-xml-file-for-object-detection-with-opencv-6932e22c3f0e
    robot_detection_data = cv2.CascadeClassifier("cascade.xml")
    
    found = robot_detection_data.detectMultiScale(img_gray, minNeighbors=9, minSize=(20, 20))
    
    return found


def draw_detection(img, found:list) -> None:
    """
    Shows image with object outlined in found. found is list of [[x,y,width,height], ...]
    """

    img = cv2.imread(img)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    amount_found = len(found)

    if amount_found != 0:
        for (x, y, width, height) in found:
            # draw a green rectangle around every detected object
            cv2.rectangle(img_rgb, (x, y), (x + height, y + width), DETECTION_COLOUR, DETECTION_THICKNESS)

    # show image using matplotlib
    plt.subplot(1, 1, 1)
    plt.imshow(img_rgb)
    plt.show()


def calculate_distance(detected_objects:list):
    """
    Calculates the approximate distance to the object in the image
    """
    CAMERA_WIDTH = 1920 #pixel width
    CAMERA_CONSTANT = 1 #depends on focal length of camera
    
    if len(detected_objects) > 0:
        for x,y,width,height in detected_objects:
            mid_x = x + (width/2)
            mid_y = y + (height/2)
            
            distance_to_robot = CAMERA_CONSTANT / height #distance in mm
            
            print(distance_to_robot)
            
            if distance_to_robot < 500: #if robot is closer than 50cm
            
                if mid_x < (CAMERA_WIDTH/2): #if robot to the left
                    print("move right")
                    
                if mid_x > (CAMERA_WIDTH/2):  #if robot to the right
                    print("move left")