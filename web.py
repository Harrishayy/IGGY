from flask import Flask, redirect, url_for, render_template, request, session, Request, jsonify
from robot import Robot


app = Flask(__name__)
app.secret_key = "supersecretkey"
robot = Robot()

@app.route("/")
def home():
    return redirect("/robot/")


@app.route("/robot/")
def main_page():
    return render_template("robot.html")


@app.route("/robot-move", methods=["POST"])
def robot_forward():

    return jsonify({"response":"moving..."})




if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")