# read face_data.json and remove student from the json given the student id
def main():
    import json
    import os

    with open('data/face_data.json') as f:
        data = json.load(f)

    student_id = input("Enter the student id: ")

    # remove the student from the json
    for i in range(len(data)):
        if data[i]['studentId'] == student_id:
            del data[i]
            print(f"Student id: {student_id} has been removed")
            break

    # write the updated json to the file
    with open('data/face_data.json', 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()
