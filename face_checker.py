"""
pip install face_recognition
pip install opencv-python
pip install numpy
"""
import csv
import logging
from datetime import datetime

import cv2
import face_recognition

# Configure logging
logging.basicConfig(filename='logs/authentication.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

# Initialize the CSV file variable with None
csv_file = None


# Initialize the camera (0 is usually the default camera, but you can change it if needed)
video_capture = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not video_capture.isOpened():
    logging.error("Could not open camera.")
else:
    try:
        # Load face recognition images and encodings
        user1_image = face_recognition.load_image_file("photos/user1.jpg")
        user1_encoding = face_recognition.face_encodings(user1_image)[0]

        user2_image = face_recognition.load_image_file("photos/user2.jpg")
        user2_encoding = face_recognition.face_encodings(user2_image)[0]

        user3_image = face_recognition.load_image_file("photos/user3.jpg")
        user3_encoding = face_recognition.face_encodings(user3_image)[0]

        user4_image = face_recognition.load_image_file("photos/user4.jpg")
        user4_encoding = face_recognition.face_encodings(user4_image)[0]

        user5_image = face_recognition.load_image_file("photos/captured_image_10.jpg")
        user5_encoding = face_recognition.face_encodings(user4_image)[0]

        known_face_encodings = [
            user1_encoding, user2_encoding, user3_encoding, user4_encoding, user5_encoding
        ]

        known_face_names = [
            'Bob',
            'John',
            'Natasha',
            'Nikita'
        ]

        students = list(known_face_names)

        # Initialize variables
        face_locations = []
        face_encodings = []
        face_names = []
        capturing = False

        # Get time
        now = datetime.now()
        current_date = now.strftime("%d-%m-%Y")

        # Store into CSV file
        csv_file = open(current_date + '.csv', 'w+', newline='')
        csv_writer = csv.writer(csv_file)

        while True:
            ret, frame = video_capture.read()

            if not ret:
                logging.error("Could not capture a frame from the camera.")
                break

            # Resize the frame
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert BGR frame to RGB for face recognition
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Only process every other frame to save processing time
            if capturing:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]

                    face_names.append(name)

                    if name in students:
                        students.remove(name)
                        print(students)
                        current_time = now.strftime("%H-%M-%S")
                        csv_writer.writerow([name, current_time])

            capturing = not capturing

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            cv2.imshow('Face Recognition', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        logging.exception("An error occurred: %s", str(e))

    finally:
        # Release the camera and close OpenCV windows
        video_capture.release()
        cv2.destroyAllWindows()

        # Close the CSV file
        csv_file.close()
