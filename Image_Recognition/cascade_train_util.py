import os

DIRECTORY = os.path.dirname(os.path.realpath(__file__))

DATASET_DIRECTORY = DIRECTORY + "/Image_Dataset"

def generate_negative_description_file():
    with open(DATASET_DIRECTORY + "/negative.txt", "w") as file:
        for file_name in os.listdir(DATASET_DIRECTORY + "/Negative"):
            file_name = file_name.replace(" ", "_")
            file.write("Image_Dataset/Negative/" + file_name + "\n")
            
    print("Generated Negative Image Text File")
    
def remove_spaces_from_images():
    for file_name in os.listdir(DATASET_DIRECTORY + "/Positive"):
        old_directory = DATASET_DIRECTORY + "/Positive/" + file_name
        new_directory = DATASET_DIRECTORY + "/Positive/" + file_name.replace(" ", "_")
        os.rename(old_directory, new_directory)
        
    for file_name in os.listdir(DATASET_DIRECTORY + "/Negative"):
        old_directory = DATASET_DIRECTORY + "/Negative/" + file_name
        new_directory = DATASET_DIRECTORY + "/Negative/" + file_name.replace(" ", "_")
        os.rename(old_directory, new_directory)
            
    
            
if __name__ == "__main__":
    generate_negative_description_file()
