import os
import pickle

from Controller.DatabaseManager import DatabaseManager
from Controller.EncodeManager import EncodeManager
from Model.User import User


class UserManager:

    def __init__(self):

        self.db_mngr = DatabaseManager()
        self.encoder = EncodeManager()

    def recognize_user(self, img_snap):

        self.embeddings_unknown = self.encoder.encode_img(img_snap)
        if len(self.embeddings_unknown) == 0:
            return 'no_persons_found'
        else:
            self.embeddings_unknown = self.embeddings_unknown[0]

        user_arrays = self.db_mngr.get_usr_encod_as_arr()

        if user_arrays:
            for user_t_number, embedding in user_arrays:

                # match = face_recognition.compare_faces([embedding], self.embeddings_unknown)[0]
                match = self.encoder.match_encodings(embedding, self.embeddings_unknown)

                if match:
                    print(f"User t_number: {user_t_number}")
                    return user_t_number
                else:
                    db_path = 'bucket'
                    self.embeddings_unknown = self.encoder.encode_img(img_snap)
                    if len(self.embeddings_unknown) == 0:
                        return 'no_persons_found'
                    else:
                        self.embeddings_unknown = self.embeddings_unknown[0]

                    db_dir = sorted(os.listdir(db_path))

                    match = False
                    j = 0
                    while not match and j < len(db_dir):
                        path_ = os.path.join(db_path, db_dir[j])

                        file = open(path_, 'rb')
                        embeddings = pickle.load(file)

                        # match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]
                        match = self.encoder.match_encodings(embeddings, self.embeddings_unknown)
                        j += 1

                    if match:
                        return db_dir[j - 1][:-7]
                    else:
                        print(f"User t_number: {db_dir[j - 1][:-7]}")
                        return 'unknown_person'
        else:
            print("No user encodings found.")
            return 'no_persons_found'

    def login(self, img_snap):
        result = self.recognize_user(img_snap)
        if result in ['unknown_person', 'no_persons_found']:
            return False
        else:
            return result

    def logout(self, img_snap):
        result = self.recognize_user(img_snap)
        if result in ['unknown_person', 'no_persons_found']:
            return False
        else:
            return result

    def register_new_user(self, user_t_num, user_name, attendance_qty, user_role, user_img_encode):
        user = User(str(user_t_num).lower(), str(user_name).lower(), attendance_qty, str(user_role).lower(),
                    user_img_encode)

        self.db_mngr.insert_user(user)
        # check if user was created
        if self.db_mngr.find_user(user_t_num) is not None:
            return True
        else:
            self.db_mngr.close_connection()
            return False

    def get_name_by_id(self, t_number):
        return self.db_mngr.get_name_with_t_no(t_number)
