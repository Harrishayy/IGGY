import os
import cv2

import time


class Annotate():
    def __init__(self) -> None:
        self.file_directory = os.path.dirname(os.path.realpath(__file__))
        self.current_image = None
        self.already_processed = None
        self.update_already_processed()
        self.selected = []
        self.alternate_first_second = False #used to switch between setting the first and second coordinate
        self.mouse_click_coords = None
        self.mouse_click_coords2 = None


    def exit(self):
        cv2.destroyAllWindows()
        

    def next_image(self) -> None:
        for img in self.get_positive_images():
            if img not in self.already_processed:
                self.current_image = img
                return
            
        self.current = None    
        print("All images have been processed!")
        self.exit() #only runs if all images run out


    def save_current(self) -> None:
        img_directory = r"Image_Dataset/Positive/" + self.current_image
        pos_directory = self.file_directory + r"/Image_Dataset/positive.txt"

        selected_details = ""
        for coordinates in self.selected:
            selected_details += f"{coordinates[0][0]} {coordinates[0][1]} {coordinates[1][0]} {coordinates[1][1]} "

        pos_details = f"{img_directory} {len(self.selected)} {selected_details[:-1]}"

        with open(pos_directory, "r") as pos_file:
            text = pos_file.read()

        with open(pos_directory, "a") as pos_file:
            if not text.endswith("\n"):
                pos_file.write("\n")

            pos_file.write(pos_details)


    def confirm_selection(self) -> None:
        self.selected.append([self.mouse_click_coords, self.mouse_click_coords2])


    def remove_last_selected(self) -> None:
        if len(self.selected) > 0:
            self.selected.pop()


    def draw_selected(self,img):
        if len(self.selected) > 0:
            for [(x1,y1),(x2,y2)] in self.selected:
                img = cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 1)

        return img


    def handle_mouse_event(self,event,x,y,flags,param):
        self.mouseX = x #saves current position of mouse
        self.mouseY = y

        if event == cv2.EVENT_LBUTTONDOWN: #detects if left mouse button is pressed
            if self.alternate_first_second == True:
                self.mouse_click_coords2 = (x,y)
                self.alternate_first_second = False
            else:
                self.mouse_click_coords = (x,y)
                self.mouse_click_coords2 = None
                self.alternate_first_second = True


    def get_positive_images(self) -> list:
        pos_directory = self.file_directory + r"/Image_Dataset/Positive/"

        pos_imgs = os.listdir(pos_directory)

        return pos_imgs


    def update_already_processed(self) -> None:
        pos_directory = self.file_directory + r"/Image_Dataset/positive.txt"

        with open(pos_directory, "r") as pos_file:
            pos_imgs = pos_file.readlines()

        already_processed = []

        for img_details in pos_imgs:
            img_file = img_details.split(" ")[0]
            img_file_name = img_file.split("/")[-1].split("\\")[-1]

            already_processed.append(img_file_name)

        self.already_processed = already_processed


    def get_image_data(self, img_name):
        if img_name is None:
            self.exit()

        img_directory = self.file_directory + r"/Image_Dataset/Positive/" + img_name
        img = cv2.imread(img_directory)
        return img
        

    def display_image(self, img) -> None:
        cv2.imshow("Annotation Tool", img)
        

    def run(self) -> None:
        self.next_image()
        img = self.get_image_data(self.current_image)
        self.display_image(img)
        cv2.setMouseCallback("Annotation Tool", self.handle_mouse_event)

        while True:
            img = self.get_image_data(self.current_image)

            if self.mouse_click_coords is not None and self.mouse_click_coords2 is None:
                img = cv2.rectangle(img, self.mouse_click_coords, (self.mouseX, self.mouseY), (0,0,255), 1)

            elif self.mouse_click_coords is not None and self.mouse_click_coords2 is not None:
                img = cv2.rectangle(img, self.mouse_click_coords, self.mouse_click_coords2, (0,0,255), 1)

            img = self.draw_selected(img)
            self.display_image(img)

            key_press = cv2.waitKey(1) #waits a milisecond for key press in every loop

            if key_press == ord("q") or key_press == 27:
                break

            elif key_press == ord("c"):
                self.confirm_selection()

            elif key_press == ord("d"):
                self.remove_last_selected()

            elif key_press == ord("n"):
                self.save_current() #updates positive.txt file to store
                self.update_already_processed() #updates the images which have already been processed so the same image isnt shown twice
                self.next_image() #displays the next image
                self.selected = [] #resets the currently selected objects
                self.mouse_click_coords = None
                self.mouse_click_coords2 = None

        self.exit()

if __name__ == "__main__":
    annotate = Annotate()
    annotate.run()
