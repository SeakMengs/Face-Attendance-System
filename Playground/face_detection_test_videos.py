import cv2
import os

# Load the pre-trained Haar cascade XML file
cascade_path = 'cascade28\cascade.xml'
# cascade_path = 'cascadeRecord\cascade.xml'
# cascade_path = 'pre-train\haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

# video sample credit: https://github.com/intel-iot-devkit/sample-videos?tab=readme-ov-file
# Open a connection to the webcam (0 represents the default webcam)
# cap = cv2.VideoCapture('test_videos\\face-demographics-walking.mp4')
cap = cv2.VideoCapture('test_videos\\face-demographics-walking-and-pause.mp4')

while cap.isOpened():
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Perform face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display the result
    cv2.imshow('Face Detection', frame)

    # Break the loop if the user clicks the close button on the window
    if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ASCII code for the 'Esc' key
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
