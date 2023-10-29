import datetime
import os.path
import pickle
import tkinter as tk

import cv2
import face_recognition
from PIL import Image, ImageTk

import util




class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x600+350+100")

        self.login_btn = util.create_btn(self.main_window, 'login', 'green', self.login)
        self.login_btn.place(x=850, y=200)

        self.logout_btn = util.create_btn(self.main_window, 'logout', 'red', self.logout)
        self.logout_btn.place(x=850, y=300)

        self.new_user_reg = util.create_btn(self.main_window, 'register new user', 'gray',
                                            self.register_new_user, fg='black')
        self.new_user_reg.place(x=850, y=400)

        self.cam_frame = util.get_img_label(self.main_window)
        self.cam_frame.place(x=20, y=20, width=750, height=500)

        self.start_webcam(self.cam_frame)

        # Create a folder where the images will be stored
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

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

    def login(self):

        name = util.recognize(self.img_snap, self.db_dir)

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
        else:
            util.msg_box('Welcome back !', 'Welcome, {}.'.format(name))
            with open(self.log_path, 'a') as f:
                f.write('{},{},in\n'.format(name, datetime.datetime.now()))
                f.close()

    def logout(self):
        name = util.recognize(self.img_snap, self.db_dir)

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
        else:
            util.msg_box('See you soon!', 'Goodbye, {}.'.format(name))
            with open(self.log_path, 'a') as f:
                f.write('{},{},out\n'.format(name, datetime.datetime.now()))
                f.close()

    def register_new_user(self):
        self.registration_window = tk.Toplevel(self.main_window)
        self.registration_window.geometry("1200x520+370+120")

        self.accept_btn = util.create_btn(self.registration_window, 'Accept', 'green',
                                          self.accept_register_new_user)
        self.accept_btn.place(x=750, y=300)

        self.try_again_btn = util.create_btn(self.registration_window, 'Try again',
                                             'orange', self.repeat_registration)
        self.try_again_btn.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.registration_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.user_name_input = util.get_entry_text(self.registration_window)
        self.user_name_input.place(x=750, y=150)

        self.registration_txt_label = util.get_text_label(self.registration_window,
                                                          'Registration Form:')
        self.registration_txt_label.place(x=750, y=70)

    def repeat_registration(self):
        self.registration_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.recent_capture)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.new_user_capture = self.img_snap.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        user_name = self.user_name_input.get(1.0, "end-1c")

        user_img_encode = face_recognition.face_encodings(self.new_user_capture)[0]

        file = open(os.path.join(self.db_dir, '{}.pickle'.format(user_name)), 'wb')
        pickle.dump(user_img_encode, file)
        self.registration_window.destroy()
        util.msg_box('Success!', 'User was registered successfully !')


if __name__ == "__main__":
    app = App()
    app.start()
