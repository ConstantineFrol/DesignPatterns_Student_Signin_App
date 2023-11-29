import os
import pickle

import face_recognition

from Controller.DatabaseManager import DatabaseManager
from Model.User import User
from Utilities.FileManager import FileManager
from Utilities.LogManager import LogManager


class UserManager:

    def __init__(self):
        """Initialize UserManager."""
        self.file_manager = FileManager()
        self.db_mngr = DatabaseManager()
        self.user_log = LogManager(self.file_manager.get_path('u_logs'))
        self.err_log = LogManager(self.file_manager.get_path('er_logs'))
        self.embeddings_unknown = []

    def recognize_user(self, img_snap):
        """Recognize a user based on face recognition in the provided image snapshot."""
        # global self.embeddings_unknown
        try:
            self.embeddings_unknown = face_recognition.face_encodings(img_snap)
        except Exception as e:
            self.err_log.log_error(f"Check the camera connection in {self.__class__.__name__}.py - {str(e)}")
        if len(self.embeddings_unknown) == 0:
            return 'no_persons_found'
        else:
            embeddings_unknown = self.embeddings_unknown[0]

        user_arrays = self.db_mngr.get_usr_encod_as_arr()

        if user_arrays:
            for user_t_number, embedding in user_arrays:
                match = face_recognition.compare_faces([embedding], embeddings_unknown)[0]

                if match:
                    print(f"User t_number: {user_t_number}")
                    return user_t_number
                else:
                    db_path = 'bucket'
                    embeddings_unknown = face_recognition.face_encodings(img_snap)

                    if len(embeddings_unknown) == 0:
                        return 'no_persons_found'
                    else:
                        embeddings_unknown = embeddings_unknown[0]

                    db_dir = sorted(os.listdir(db_path))

                    match = False
                    j = 0
                    while not match and j < len(db_dir):
                        path_ = os.path.join(db_path, db_dir[j])
                        file = open(path_, 'rb')
                        embeddings = pickle.load(file)

                        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]
                        j += 1

                    if match:
                        return db_dir[j - 1][:-7]
                    else:
                        return 'unknown_person'
        else:
            print("No user encodings found.")
            return 'no_persons_found'

    def login(self, img_snap):
        """Login a user based on face recognition in the provided image snapshot."""
        result = self.recognize_user(img_snap)

        if result in ['unknown_person', 'no_persons_found']:
            return False
        else:
            self.user_name = self.db_mngr.get_name_with_t_no(result)
            print(f"User:\tid:{result}, name:{self.user_name}\tlogged in.")
            self.db_mngr.modify_attendance(result, 1)
            self.user_log.log_info(f"User:\tid:{result}, name:{self.user_name}\tlogged in.")
            return result

    def logout(self, img_snap):
        """Logout a user based on face recognition in the provided image snapshot."""
        result = self.recognize_user(img_snap)

        if result in ['unknown_person', 'no_persons_found']:
            return False
        else:
            self.user_name = self.db_mngr.get_name_with_t_no(result)
            self.user_log.log_info(f"User:\tid:{result}, name:{self.user_name}\tlogged out.")
            return result

    def register_new_user(self, user_t_num, user_name, attendance_qty, user_role, user_img_encode):
        """Register a new user with the provided information."""
        user = User(str(user_t_num).lower(), str(user_name).lower(), attendance_qty, str(user_role).lower(),
                    user_img_encode)

        self.db_mngr.insert_user(user)

        # Check if the user was created
        if self.db_mngr.find_user(user_t_num) is not None:
            print(f"New Registration:\tid:{user_t_num}, name:{str(user_name).lower()}.")
            self.user_log.log_info(f"New Registration:\tid:{user_t_num}, name:{str(user_name).lower()}.")
            return True
        else:
            self.db_mngr.close_connection()
            return False
