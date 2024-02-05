import cv2
import os

def detect_face(frame):
        # Convert the frame to grayscale for face detection
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Perform face detection
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Display the result
        cv2.imshow('Face Detection', frame)
        cv2.waitKey(0)
    
if __name__ == '__main__':
    # Load the pre-trained Haar cascade XML file
    cascade_path = 'cascade\cascade.xml'
    # cascade_path = 'cascadeRecord\cascade.xml'
    # cascade_path = 'pre-train\haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    img1 = cv2.imread('test_images\\family1.jpg', cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread('test_images\\family2.jpg', cv2.IMREAD_GRAYSCALE)
    img3 = cv2.imread('test_images\\family3.jpg', cv2.IMREAD_GRAYSCALE)

    detect_face(img1)
    detect_face(img2)
    detect_face(img3)

    # close all windows
    cv2.destroyAllWindows()
