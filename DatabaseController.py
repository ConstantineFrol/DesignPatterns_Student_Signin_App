import json
from datetime import datetime

import face_recognition
import firebase_admin
import numpy as np
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("Keys/attendanceapp-14ff7-firebase-adminsdk-2ad5k-86b6c1ff77.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendanceapp-14ff7-default-rtdb.europe-west1.firebasedatabase.app/"
})

reference = db.reference('users')


def upload_user_to_database(user):
    # Convert the user.encode (NumPy ndarray) to a Python list
    encode_list = user.encode.tolist()

    # Create a dictionary with user data
    user_data = {
        "name": user.name,
        "email": user.email,
        "t_number": user.t_number,
        "image_path": user.image_path,
        "role": user.role,
        "encode": json.dumps(encode_list),
        "registered": user.registered,
        "total_attendance": user.total_attendance,
        "last_attendance": user.last_attendance
    }

    # Push the user data to the database
    new_user_ref = reference.push()
    new_user_ref.set(user_data)
    return new_user_ref.key


def print_all_user_ids():
    user_data = reference.get()
    if user_data is not None and "users" in user_data:
        users_data = user_data["users"]
        for user_id in users_data:
            print("User ID:", user_id)

    else:
        print('NONE KURVA !!!!!')


def update_attendance(user_id):
    # Find the user in the database with the given user_id
    print('Searching for ID')
    user_ref = reference.child("users")
    user_data = user_ref.get()

    if user_data is not None:
        current_datetime = datetime.now()

        # Get user information
        name = user_data.get("name")
        t_number = user_data.get("t_number")
        role = user_data.get("role")
        total_attendance = user_data.get("total_attendance")

        # Update attendance information
        if total_attendance is not None:
            total_attendance = int(total_attendance) + 1
        else:
            total_attendance = 1

        last_attendance = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # Update the database with the new attendance information for the specific user
        user_ref.update({
            "total_attendance": total_attendance,
            "last_attendance": last_attendance
        })

        # Print user information
        print(f"User Name: {name}")
        print(f"T_Number: {t_number}")
        print(f"Role: {role}")
        print(f"Total Attendance: {total_attendance}")
        print(f"Last Attendance: {last_attendance}")
    else:
        print(f"User with ID {user_id} not found in the database")


def match_users(encode):
    matched_users = []

    # Fetch all user data from the database
    user_data = reference.get()

    if user_data is not None:
        for user_id, user_info in user_data.items():
            t_number = user_info.get("t_number")
            user_name = user_info.get("name")
            user_encode = user_info.get("encode")

            if t_number and user_encode:
                # Check if the "encode" value is a non-empty string
                if isinstance(user_encode, str) and user_encode:
                    # Convert the JSON-encoded encoding to a Python list
                    db_user_encode_list = json.loads(user_encode)

                    try:
                        # Convert the user's encoding to a NumPy array
                        db_user_encode_np = np.array(db_user_encode_list, dtype=float)
                        encode_np = np.array(encode, dtype=float)

                        # Compare the given encoding with the user's encoding
                        matches = face_recognition.compare_faces([db_user_encode_np], encode_np)

                        # If there's a match
                        if any(matches):
                            print(f"WOO-HOO - - - Matched User: Name - {user_info.get('name')}, "
                                  f"T_Number - {user_info.get('t_number')}"
                                  )
                            # TODO IT CAN DETECT FROM DATABASE, BUT CAN'T FIND USER BY NODE ID :(
                            update_attendance(user_id)

                            print_all_user_ids()

                    except ValueError as e:
                        print(f"User encode is invalid: {e}")
                else:
                    print(f"User encode is empty or not a string")

    # for user in matched_users:
    # print(f"WOO-HOO - - - Matched User: Name - {user.name}, T_Number - {user.t_number}")

    # return matched_users
