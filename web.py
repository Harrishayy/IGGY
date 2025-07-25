from flask import Flask, redirect, url_for, render_template, request, session, Request, jsonify, Response
from robot import Robot
from object_recognition import detect_object, draw_detection
import cv2
import math


app = Flask(__name__)
app.secret_key = "qUYlpm55JRqJN5VQjgQaxnMTxrsLuZL8" #randomly generated 32 character string with base 62
robot = Robot(debug=False)
#robot.shutdown()

@app.route("/")
def home():
    return redirect("/robot/")


@app.route("/robot/")
def main_page():
    robot.initialise()
    robot.run()
    return render_template("robot.html")


@app.route("/kill/")
def terminate():
    robot.motor_board.stop()
    robot.shutdown()
    return redirect(url_for("main_page"))


@app.route("/autonomous")
def autonomous_mobility():
    robot.autonomous()
    return jsonify({"response":"Initiating autonomous control"})


@app.route("/robot-move", methods=["POST"])
def robot_move():
    if request.method == "POST":
        speed = request.json["speed"]
        direction = request.json["direction"]

        if speed != '':
            speed = int(speed)
        else:
            speed = 0

        match direction:
            case "w":
                robot.motor_board.forward(speed)

            case "s":
                robot.motor_board.backward(speed)

            case "a":
                robot.motor_board.left(speed)

            case "d":
                robot.motor_board.right(speed)

            case "stop":
                robot.following = False
                robot.motor_board.stop()

            case "auto":
                robot.autonomous()

    s = speed, direction

    return jsonify({"Message":s})


@app.route("/accelerometer", methods=["POST"])
def acc():
    data = robot.read_accelerometer()

    ax,ay,az=data[0],data[1],data[2]

    mag = ax*ax + ay*ay + az*az

    if (mag > 10):
        robot.emote.emotion_state("sad")



    return jsonify({"log":data})


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

    try:
        robot.shutdown()
    except Exception as e:
        print("Error shutting down robot:\n" + e)