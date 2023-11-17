import datetime

import face_recognition

import util
from Controller.DatabaseManager import DatabaseManager
from View.UIManager import UIManager


class App:
    def __init__(self):
        self.main_window = UIManager()

        self.main_window.create_window('Home Screen', '1200x600+350+100')

        self.login_btn = self.main_window.create_btn('Login', 'green', self.login)
        self.login_btn.place(x=850, y=200)

        self.logout_btn = self.main_window.create_btn('Logout', 'red', self.logout)
        self.logout_btn.place(x=850, y=300)

        self.registration_btn = self.main_window.create_btn('Register New User', 'gray', self.register_new_user,
                                                            fg='black')
        self.registration_btn.place(x=850, y=400)

        self.camera_label = self.main_window.create_label(self.main_window)
        self.camera_label.place(x=20, y=20, width=750, height=500)

        # self.start_webcam(self.camera_label)

        self.log_path = './Logs/user_log.txt'
        self.db_connection = DatabaseManager()

    def login(self):
        # TODO: implement login
        t_number = self.recognize_user(self.img_snap, self.db_connection)

        if t_number in ['unknown_person', 'no_persons_found']:
            self.main_window.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
        else:
            self.main_window.msg_box('Welcome back !', 'Welcome, {}.'.format(name))
            with open(self.log_path, 'a') as f:
                f.write('{},{},in\n'.format(name, datetime.datetime.now()))
                f.close()

    def logout(self):
        name = util.recognize(self.img_snap, self.db_dir)

        if name in ['unknown_person', 'no_persons_found']:
            self.main_window.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
        else:
            self.main_window.msg_box('See you soon!', 'Goodbye, {}.'.format(name))
            with open(self.log_path, 'a') as f:
                f.write('{},{},out\n'.format(name, datetime.datetime.now()))
                f.close()

    def start(self):
        print("Starting app...")
        self.main_window.mainloop()

    def recognize_user(img, db_connection):

        embeddings_unknown = face_recognition.face_encodings(img)
        if len(embeddings_unknown) == 0:
            return 'no_persons_found'

        embeddings_unknown = embeddings_unknown[0]

        all_users_encode = db_connection.get_all_users_encode()

        match = False
        user_id = 'unknown_person'

        for t_number, encode in all_users_encode:
            match = face_recognition.compare_faces([encode], embeddings_unknown)[0]
            if match:
                user_id = t_number
                break

        return user_id


if __name__ == "__main__":
    app = App()
    app.start()
