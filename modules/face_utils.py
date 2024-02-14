import datetime
import os
import time
import cv2
from numba import jit
import json
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from tkinter import messagebox

cascade_path = 'data/haarcascade_frontalface_default.xml'
MAX_FACES_RECORD = 100
FACE_JSON_FILE_NAME = 'face_data.json'
COL = ['Student_ID', 'Name', 'Date', 'Time']


@jit(nopython=True)
def add_face_percentage(current_face_data: int) -> float:
    return current_face_data / MAX_FACES_RECORD * 100


def save_face_data(face_data: list, name: str, studentId: str) -> bool:
    if len(face_data) == 0:
        print("No face data to save")
        return False

    if not os.path.exists('data'):
        os.makedirs('data')

    if FACE_JSON_FILE_NAME not in os.listdir('data'):
        # create new file and write data
        with open('data/face_data.json', 'w') as f:
            json_data = [{
                'name': name,
                'studentId': studentId,
                'face_data': face_data
            }]
            json.dump(json_data, f)
    else:
        # read file and append data
        with open('data/face_data.json', 'r') as f:
            json_data = json.load(f)
            # update exsiting data if studentId already exists else append new data
            for student in json_data:
                if student['studentId'] == studentId:
                    student['name'] = name
                    student['face_data'] = face_data
                    break
            else:
                json_data.append({
                    'name': name,
                    'studentId': studentId,
                    'face_data': face_data
                })

        with open('data/face_data.json', 'w') as f:
            json.dump(json_data, f)
    return True


def load_face_data() -> list:
    try:
        with open('data/face_data.json', 'r') as f:
            json_data = json.load(f)
        return json_data
    except:
        messagebox.showerror("Error", "Failed to load face data!")
        return []


def add_face(name: str, studentId: str, webcamIndex: int) -> bool:
    if len(name) == 0 or len(studentId) == 0:
        print("Name or Student ID cannot be empty")
        return False

    if webcamIndex < 0:
        webcamIndex = 0

    face_data = []
    i = 0

    cap = cv2.VideoCapture(webcamIndex)
    face_cascade = cv2.CascadeClassifier(cascade_path)

    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.05, minNeighbors=6, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # crop image, [y:y+h, x:x+w] = [height, width]
            crop_img = frame[y:y+h, x:x+w]
            # resize image to 50x50
            resized_img = cv2.resize(crop_img, (50, 50))
            if len(face_data) <= MAX_FACES_RECORD and i % 10 == 0:
                face_data.append(resized_img.tolist())
            i = i+1

            # org = origin
            cv2.putText(img=frame, text=f"Recording face {round(add_face_percentage(len(face_data)))}%", org=(
                x, y-10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 255, 0), thickness=2)
            cv2.rectangle(img=frame, pt1=(x, y), pt2=(x+w, y+h),
                          color=(0, 255, 0), thickness=2)

        cv2.imshow('Add Face', frame)

        if cv2.waitKey(delay=1) == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            print("Face recording stopped, not saving data")
            return False

        if len(face_data) >= MAX_FACES_RECORD:
            print("Face recording stopped, saving data")
            break

    cap.release()
    cv2.destroyAllWindows()

    face_data = np.array(face_data)
    # convert 3D array to 2D array
    face_data = face_data.reshape((face_data.shape[0], -1))
    face_data = face_data.tolist()

    return save_face_data(face_data, name, studentId)


def find_student_by_id(studentId, students) -> str:
    for student in students:
        if student['studentId'] == studentId:
            return student['name']
    return "Unknown"


def get_today_date() -> str:
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y')


def get_today_time() -> str:
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')


def load_attendances(date: str = get_today_date()):
    try:
        filename = f'attendance_{date}.csv'
        if filename not in os.listdir('attendances'):
            return []
        df = pd.read_csv(f'attendances/{filename}')
        return df
    except:
        return []


def save_attendance(student_id) -> bool:
    if len(student_id) == 0:
        print("Student ID cannot be empty")
        return False

    if not os.path.exists('attendances'):
        os.makedirs('attendances')

    student_name = find_student_by_id(student_id, load_face_data())
    attendance = [student_id, student_name, get_today_date(), get_today_time()]
    attendances = load_attendances()
    filename = f'attendance_{get_today_date()}.csv'

    if len(attendances) == 0:
        if filename not in os.listdir('attendances'):
            df = pd.DataFrame(columns=COL)
            df.loc[0] = attendance
            df.to_csv(f'attendances/{filename}', index=False)
            print(
                f"Student Id: {student_id}, Name: {student_name}, Attendance marked")
            return True

    for _student_id in attendances[COL[0]]:
        if str(_student_id) == str(student_id):
            print(
                f"Student Id: {student_id}, Name: {student_name}, Attendance already marked")
            return True

    df = pd.DataFrame(columns=COL)
    df.loc[0] = attendance
    df.to_csv(f'attendances/{filename}', mode='a', header=False, index=False)
    print(f"Student Id: {student_id}, Name: {student_name}, Attendance marked")
    return True


def face_attendance(webcamIndex: int) -> bool:
    if webcamIndex < 0:
        webcamIndex = 0

    json_data = load_face_data()

    if len(json_data) == 0:
        print("No face data found")
        return False
    knn = KNeighborsClassifier(n_neighbors=5)
    x = []
    y = []
    for student in json_data:
        for face in student['face_data']:
            x.append(face)
            y.append(student['studentId'])

    knn.fit(x, y)

    cap = cv2.VideoCapture(webcamIndex)
    face_cascade = cv2.CascadeClassifier(cascade_path)
    detected_students = {}

    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.05, minNeighbors=6, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # crop image, [y:y+h, x:x+w] = [height, width]
            crop_img = frame[y:y+h, x:x+w]
            # resize image to 50x50
            resized_img = cv2.resize(crop_img, (50, 50)).reshape(1, -1)
            prediction = knn.predict(resized_img)
            student_id = prediction[0]

            if student_id not in detected_students:
                detected_students[student_id] = {}
                detected_students[student_id]['name'] = find_student_by_id(
                    student_id, json_data)
                detected_students[student_id]['attendance'] = save_attendance(
                    student_id)

            cv2.putText(img=frame, text=f"Student ID: {student_id}, Name: {detected_students[student_id]['name']}", org=(
                x, y-10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 255, 0), thickness=2)
            cv2.putText(img=frame, text=f"Attendance: {'marked' if detected_students[student_id]['attendance'] else 'not marked yet'}", org=(
                x, y-30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 255, 0), thickness=2)
            cv2.rectangle(img=frame, pt1=(x, y), pt2=(x+w, y+h),
                          color=(0, 255, 0), thickness=2)

        cv2.imshow('Face Attendance', frame)

        if cv2.waitKey(delay=1) == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            print("Face attendance stopped")
            return True
