import cv2
import numpy as np

DETECTION_COLOUR = (255,0,255)
DETECTION_THICKNESS = 2
FPS = 24

FONT = cv2.FONT_HERSHEY_COMPLEX
FONTSCALE = 0.5
FONTCOLOUR = (255,0,255)
FONTTHICKNESS = 2
LINETYPE = 2
TEXTOFFSET = 2*FONTTHICKNESS + 3


#Camera settings for logitech c270
CAMERA_WIDTH = 1920 #px
CAMERA_HEIGHT = 1080 #px
FOCAL_LENGTH = 4 # 4.0mm
CAMERA_SENSOR_HEIGHT = 3.58 # 3.58mm
ROBOT_ESTIMATED_HEIGHT = 500 # max robot height is 500mm

# distance_to_robot = (FOCAL_LENGTH * ROBOT_ESTIMATED_HEIGHT * CAMERA_HEIGHT) / (height * CAMERA_SENSOR_HEIGHT)
# distance becomes (CAMERA_CONSTANT / height) of robot in px
CAMERA_CONSTANT = (FOCAL_LENGTH * ROBOT_ESTIMATED_HEIGHT * CAMERA_HEIGHT) /  CAMERA_SENSOR_HEIGHT

def detect_robot(img_data) -> list:
    """
    Returns an array of tuples for the data of detected robots which are (x,y,width,height) x,y = 0 at top left of screen, width and height to the right and down.
    """

    img_gray = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
    
    #the trained data for robot detection, used Cascade Trainger GUI to simplify training process but can use fully custom in code
    #tutorial for use in https://www.youtube.com/watch?v=XrCAvs9AePM
    robot_detection_data = cv2.CascadeClassifier("cascade.xml")
    
    found = robot_detection_data.detectMultiScale(img_gray, minNeighbors=10, minSize=(75, 75))
    
    return found


def draw_detection(img, found):
    if len(found) != 0:
        #repeats for every robot within the list found
        for (x, y, width, height) in found:
            #draw a rectangle around all the robots detected
            img = cv2.rectangle(img, (x, y), (x + height, y + width), DETECTION_COLOUR, DETECTION_THICKNESS)

    return img


def show_distances(img, found_robots):
    for x,y,width,height in found_robots:
        distance = round(calculate_distance(height),3)
        
        img = cv2.putText(img, f"Distance: {distance}m", (x,(y-TEXTOFFSET)), FONT, FONTSCALE, FONTCOLOUR, FONTTHICKNESS, LINETYPE)
        
    return img
    
    
def calculate_distance(height):
    distance_to_robot = CAMERA_CONSTANT / height /1000 #distance in m
            
    return distance_to_robot
    

def display_image(img):

    cv2.imshow("Computer Vision", img)

    while (True):
        if cv2.getWindowProperty("Computer Vision", cv2.WND_PROP_VISIBLE) < 1:        
            break        

        key_press = cv2.waitKey(1) #waits a milisecond for key press in every loop

        if key_press == ord("q") or key_press == 27:
            break

    cv2.destroyAllWindows()



def image_test(image_name=None):
    if image_name is None:
        raise FileNotFoundError("No image inputted")
    
    else:

        img_data = cv2.imread(image_name) #turns image into an opencv array

        found_robots = detect_robot(img_data) #detects all the robots the camera can see
        img = draw_detection(img_data, found_robots) #draws an outline of the robots
        img = show_distances(img, found_robots) #shows the distance to the robots

        display_image(img) #shows image
        
        
def sharpen_image(img):
    """
    Runs an image sharpening filter using a kernel
    """
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    img = cv2.filter2D(img, -1, kernel)
    
    return img

            
def random():
    """
    Just messing around, makes a random white noise image
    """
    import numpy as np
    while True:
        img = np.random.randint(0,255,(200,300)).astype(np.uint8)
        cv2.imshow("Noise", img)

        key_press = cv2.waitKey(1) #waits a milisecond for key press in every loop

        if key_press == ord("q") or key_press == 27:
            break

    cv2.destroyAllWindows()



if __name__ == "__main__":
    #image_test("image.png")
    
    img = cv2.imread("image.jpg")
    img = sharpen_image(img)
    display_image(img)
