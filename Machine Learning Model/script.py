# TechVidvan hand Gesture Recognizer

# import necessary packages

import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model

# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognizer model
#model = load_model('mp_hand_gesture')
model = load_model('model.h5')

# Load class names
classNames = ["left", "right", "up", "down"]


# Initialize the webcam
cap = cv2.VideoCapture(0)
each = []
while True:
    # Read each frame from the webcam
    _, frame = cap.read()

    x, y, c = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)

    # print(result)
    
    className = ''
    
    # post process the result
    if result.multi_hand_landmarks:
        landmarks =[]
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
            #each.append(landmarks)
            # Predict gesture
            
            prediction = model.predict(arg)
            #print(prediction)
            classID = np.argmax(prediction)
            className = classNames[classID]

    # show the prediction on the frame
    cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0,0,255), 2, cv2.LINE_AA)

    # Show the final output
    cv2.imshow("Output", frame) 

    if cv2.waitKey(1) == ord('q'):
        #data = np.asarray(each)
        #print(each)
        #np.save("down.npy", each)
        break

# release the webcam and destroy all active windows
cap.release()

cv2.destroyAllWindows()
