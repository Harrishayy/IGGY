from flask import Flask, redirect, url_for, render_template, request, session, Request, jsonify, Response
from robot import Robot
from object_recognition import detect_object, draw_detection
import cv2


app = Flask(__name__)
app.secret_key = "qUYlpm55JRqJN5VQjgQaxnMTxrsLuZL8" #randomly generated 32 character string with base 62
robot = Robot(debug=True)

@app.route("/")
def home():
    return redirect("/robot/")


@app.route("/robot/")
def main_page():
    return render_template("robot.html")


@app.route("/robot-move", methods=["POST"])
def robot_move():
    if request.method == "POST":
        speed = request.json["speed"]
        direction = request.json["direction"]
        time = request.json["time"]


        if speed != '':
            speed = int(speed)
        else:
            speed = 0

        if time != '':
            time = float(time)
        else:
            time = 0

        match direction:
            case 'w':
                robot.motor_board.forward(speed)

            case 's':
                robot.motor_board.backward(speed)

            case 'a':
                robot.motor_board.left(speed)

            case 'd':
                robot.motor_board.right(speed)



    s = speed, direction, time

    return jsonify({"response":s})


@app.route("/camera_feed")
def video_feed():
    """
    Web route for video streaming
    """

    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

def generate_frames():
    """
    Reads raw camera data and converts to jpg format and concatenates multiple frames
    """
    while True:
        success, frame = robot.camera.read()  # read the camera frame
        if not success:
            break
        else:

            # detect objects in current camera feed
            detected_objects = detect_object(frame)

            # draw outline of objects onto camera feed
            outlined_frame = draw_detection(frame, detected_objects)

            #convert raw data to video stream
            ret, buffer = cv2.imencode('.jpg', outlined_frame)
            outlined_frame = buffer.tobytes()

            # return frame when processed so can be sent to web client, yield will not terminate the function so allows for repeated returns

            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + outlined_frame + b'\r\n')  

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")