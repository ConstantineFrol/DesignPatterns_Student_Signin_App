import os
import pickle

import face_recognition


class EncodeManager:
    def __init__(self):
        self.encode_list = []

    def encode_img(img):
        encode = face_recognition.face_encodings(img)
        if len(encode) == 0:
            return None
        else:
            return encode[0]

    def match_encodings(user_img, encode_list):
        match = face_recognition.compare_faces(encode_list, user_img)
        return match

    def recognize(img, db_path):

        embeddings_unknown = face_recognition.face_encodings(img)
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
