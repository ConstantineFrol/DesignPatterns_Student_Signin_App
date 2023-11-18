import datetime

import cv2
import face_recognition
from PIL import Image, ImageTk

import util
from Controller.DatabaseManager import DatabaseManager
from Utilities.FileManager import FileManager
from View.UIManager import UIManager


class App:
    def __init__(self):

        self.main_window = UIManager()

        self.home_frame = self.main_window.create_window('Home Screen', '1200x600+350+100')

        self.login_btn = self.main_window.create_btn(self.home_frame, 'login', 'green', self.login)
        self.login_btn.place(x=850, y=200)

        self.logout_btn = self.main_window.create_btn(self.home_frame, 'Logout', 'red', self.logout)
        self.logout_btn.place(x=850, y=300)

        self.registration_btn = self.main_window.create_btn(self.home_frame, 'Register New User', 'gray',
                                                            self.register_new_user,
                                                            fg='black')
        self.registration_btn.place(x=850, y=400)

        self.camera_label = self.main_window.create_label(self.home_frame)
        self.camera_label.place(x=20, y=20, width=750, height=500)

        file_manager = FileManager()
        self.log_path = file_manager.get_path('logs')
        self.db_connection = DatabaseManager()
        self.start_webcam(self.camera_label)

    def start_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
            cv2.VideoCapture.set(self.cap, cv2.CAP_PROP_FRAME_WIDTH, 640)

        self._label = label
        self.get_webcam_data()

    def get_webcam_data(self):
        ret, frame = self.cap.read()

        self.img_snap = frame
        current_user_img = cv2.cvtColor(self.img_snap, cv2.COLOR_BGR2RGB)  # if webcam not working - Error
        self.recent_capture = Image.fromarray(current_user_img)
        imgtk = ImageTk.PhotoImage(image=self.recent_capture)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        # Repeat in 20 seconds
        self._label.after(20, self.get_webcam_data)

    def register_new_user(self):
        print('New user registered')

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

    def login(self):

        # t_number = self.recognize_user(self.img_snap, self.db_connection)
        #
        # if t_number in ['unknown_person', 'no_persons_found']:
        #     self.main_window.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
        # else:
        #     self.main_window.msg_box('Welcome back !', 'Welcome, {}.'.format(name))
        #     with open(self.log_path, 'a') as f:
        #         f.write('{},{},in\n'.format(name, datetime.datetime.now()))
        #         f.close()
        print('You just login')

    def logout(self):
        # name = util.recognize(self.img_snap, self.db_dir)
        #
        # if name in ['unknown_person', 'no_persons_found']:
        #     self.main_window.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
        # else:
        #     self.main_window.msg_box('See you soon!', 'Goodbye, {}.'.format(name))
        #     with open(self.lgn_det_path, 'a') as f:
        #         f.write('{},{},out\n'.format(name, datetime.datetime.now()))
        #         f.close()
        print('You just logout')

    def start(self):
        print("Starting app...")
        self.home_frame.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
