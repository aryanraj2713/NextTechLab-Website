from cgitb import text
from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import jsonify

app = Flask(__name__)
camera = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils
output = "abc"


def process_frame(frame, model):
    global output
    x, y, c = frame.shape
    frame = cv2.flip(frame, 1)

    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)

    # print(result)

    className = ''
    classNames = ["left", "right", "up", "down"]

    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for point in mpHands.HandLandmark:
                if str(point).find("INDEX_FINGER") != -1:
                    lm = handslms.landmark[point]
                    lmx = float(lm.x)
                    lmy = float(lm.y)
                    landmarks.append([lmx, lmy])

            # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

            arg = np.reshape(landmarks, (1, 8))
            # each.append(landmarks)
            # Predict gesture

            prediction = model.predict(arg)

            # print(prediction)
            classID = np.argmax(prediction)
            className = classNames[classID]

    # show the prediction on the frame
    output = className
    print(output)
    cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2, cv2.LINE_AA)
    return frame


def generate_frames(model):
    while True:

        # read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = process_frame(frame, model)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html', variable=output)


@ app.route('/video')
def video():
    model = load_model("ML model/model.h5")
    return Response(generate_frames(model), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/update', methods=['GET'])
def update():
    jsonResp = {'jack': 4098, 'sape': 4139}

    return jsonify(jsonResp)


if __name__ == "__main__":
    app.run(debug=True, port=8989)
