
All commands can be run using Git Bash Terminal or Command Prompt Terminal in the full code directory with all python files and Image Dataset inside

Positive Image Detection:

run the following command:

OPENCV_ANNOTATION_FILE_DIRECTORY --annotations=positive.txt --images=IMAGE_FOLDER_DIRECTORY

eg:
"C:\Users\tmood\OneDrive - The College of Richard Collyer\Robotics\Better Robot Recognition\OpenCV Tools\opencv_annotation.exe" --annotations="Image_Dataset/positive.txt" --images="Image_Dataset/Positive"

How to use annotation:
 - Draw rectangles around all the objects in the image
 - press c to confirm selection
 - press d to remove the last confirmed rectangle
 - press n to move to the next image when happy that ALL object have been detected in the image
 - press esc to stop, will automatically exit when all images have been processed

When finished make sure to replace all "\" with "/" in file directories
This can be done using ctrl + f in VS Code and pressing the toggle replace on the left and enter "\" and "/" in the top and bottom text boxes then press replace all



Create Samples from Positive Text File:

Open Git Bash Terminal or Command Prompt Terminal in the full code directory with all python files and Image Dataset inside and run the following command:

"C:\UCL\IGGY\Image_Recognition\OpenCV Tools\opencv_createsamples.exe" -info "C:\UCL\IGGY\Image_Recognition\Image_Dataset\positive.txt" -w 24 -h 24 -num 1000 -vec "C:\UCL\IGGY\Image_Recognition\Image_Dataset\positive.vec"


Running Training:
checks the docs at https://docs.opencv.org/3.4/dc/d88/tutorial_traincascade.html

"C:\UCL\IGGY\Image_Recognition\OpenCV Tools\opencv_traincascade.exe" --annotations="C:\UCL\IGGY\Image_Recognition\Image_Dataset\positive.txt" --images="C:\UCL\IGGY\Image_Recognition\Image_Dataset\Positive" -data "C:\UCL\IGGY\Image_Recognition\Image_Dataset\Cascade" -vec "C:\UCL\IGGY\Image_Recognition\Image_Dataset\positive.vec" -bg "C:\UCL\IGGY\Image_Recognition\Image_Dataset\negative.txt" -w 24 -h 24 -numPos 157 -numNeg 59 -numStages 20 -precalcValBufSize 4096 -precalcIdxBufSize 4096 -numThreads 8 -bt RAB -weightTrimRate 0.99 -mode ALL
