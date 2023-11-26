import os
import pickle
import tkinter as tk

import cv2
import face_recognition
import numpy as np
from PIL import ImageTk

from Controller.DatabaseManager import DatabaseManager
from Controller.UserManager import UserManager
from Utilities.FileManager import FileManager
from Utilities.LogManager import LogManager
from Utilities.WebcamManager import WebcamManager
from View.UIManager import UIManager


class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        """Initialize the main application."""
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainFrame, RegistrationFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainFrame)

    def show_frame(self, cont, user_img=None):
        """Show the requested frame."""
        frame = self.frames[cont]
        if cont == RegistrationFrame:
            frame.update_captured_image(user_img)
        frame.tkraise()


class MainFrame(tk.Frame):
    def __init__(self, parent, controller):
        """Initialize the main frame."""
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.cam = WebcamManager()
        self.usr_mngr = UserManager()
        self.main_window = UIManager()
        self.db_mngr = DatabaseManager()

        self.camera_label = self.main_window.create_label(self)
        self.camera_label.place(x=20, y=20, width=750, height=500)

        self.cam.start_webcam(self.camera_label, 0)

        self.login_btn = self.main_window.create_btn(self, 'login', 'green', self.login)
        self.login_btn.place(x=850, y=200)

        self.logout_btn = self.main_window.create_btn(self, 'Logout', 'red', self.logout)
        self.logout_btn.place(x=850, y=300)

        self.registration_btn = self.main_window.create_btn(self, 'Register New User', 'gray',
                                                            command=self.show_registration_frame,
                                                            fg='black')
        self.registration_btn.place(x=850, y=400)

    def show_registration_frame(self):
        """Show the RegistrationFrame."""
        snap = self.cam.get_user_img()
        self.controller.show_frame(RegistrationFrame, user_img=snap)

    def login(self):
        """Attempt to log in the user."""
        user_img = self.cam.get_user_snap()
        result = self.usr_mngr.login(user_img)
        if result:
            user_name = self.db_mngr.get_name_with_t_no(result)
            self.main_window.msg_box('Welcome back!', f'Welcome, {user_name}')
        else:
            self.main_window.msg_box('Ups...', 'Unknown user. Please register new user or try again.')

    def logout(self):
        """Attempt to log out the user."""
        user_img = self.cam.get_user_snap()
        result = self.usr_mngr.logout(user_img)
        if result:
            user_name = self.db_mngr.get_name_with_t_no(result)
            self.main_window.msg_box('See you soon!', 'Goodbye, {}.'.format(user_name))
        else:
            self.main_window.msg_box('Ups...', 'Unknown user. Please register new user or try again.')

    def get_snap(self):
        """Get the current snapshot from the webcam."""
        return self.cam.get_user_snap()


class RegistrationFrame(tk.Frame):
    def __init__(self, parent, controller, user_img=None):
        """Initialize the RegistrationFrame."""
        tk.Frame.__init__(self, parent)

        self.file_manager = FileManager()
        self.log_mngr = LogManager(self.file_manager.get_path('er_logs'))
        self.controller = controller
        self.label = None
        self.reg_window = UIManager()

        self.accept_btn = self.reg_window.create_btn(self, 'Accept', 'green', self.registration)
        self.accept_btn.place(x=750, y=380)

        self.try_again_btn = self.reg_window.create_btn(self, 'Try again',
                                                        'orange',
                                                        command=lambda: controller.show_frame(MainFrame))
        self.try_again_btn.place(x=750, y=450)

        self.capture_label = self.reg_window.create_label(self)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.captured_image = user_img

        self.add_label('Registration Form:', 21, x=750, y=70)

        self.add_label('Input Name:', 10, x=750, y=130)
        self.user_name_input = self.reg_window.get_entry_text(self)
        self.user_name_input.place(x=750, y=150)

        self.add_label('Input Role:', 10, x=750, y=200)
        self.user_role_input = self.reg_window.get_entry_text(self)
        self.user_role_input.place(x=750, y=220)

        self.add_label('Input T-Number:', 10, x=750, y=270)
        self.user_id_input = self.reg_window.get_entry_text(self)
        self.user_id_input.place(x=750, y=290)

    def registration(self):
        """Attempt to register a new user."""
        self.usr_mngr = UserManager()

        user_name = self.user_name_input.get(1.0, "end-1c").strip()
        user_role = self.user_role_input.get(1.0, "end-1c").strip()
        user_t_num = self.user_id_input.get(1.0, "end-1c").strip()
        self.np_image = self.img_into_np_arr(self.captured_image)
        self.current_user_img = cv2.cvtColor(self.np_image, cv2.COLOR_BGR2RGB)

        user_img_encode = face_recognition.face_encodings(self.current_user_img)[0]

        file_path = os.path.join('bucket', '{}.bucket'.format(user_t_num))
        with open(file_path, 'wb') as file:
            pickle.dump(user_img_encode, file)

        res = self.usr_mngr.register_new_user(user_t_num, user_name, 0, user_role, user_img_encode)

        if res:
            self.user_name_input.delete(1.0, "end")
            self.user_role_input.delete(1.0, "end")
            self.user_id_input.delete(1.0, "end")

            self.controller.show_frame(MainFrame)
            self.reg_window.msg_box('Success!', f'{user_name} has successfully registered !')
        else:
            self.reg_window.msg_box(f'Error', 'Error registering user.')

    def update_captured_image(self, user_img=None):
        """Update the captured image in the RegistrationFrame."""
        if user_img is None:
            self.log_mngr.log_error(f'Error: Image is None, when passing from MainApp to RegistrationFrame.')
        else:
            self.captured_image = user_img
            self.capture_label.imgtk = self.captured_image
            self.capture_label.configure(image=self.captured_image)

    def img_into_np_arr(self, img):
        """Convert the captured image to a NumPy array."""
        pil_image = ImageTk.getimage(img)
        return np.array(pil_image)

    def add_label(self, text, font_size, **kwargs):
        """Add a label to the RegistrationFrame."""
        self.label = self.reg_window.get_text_label(self, text, font_size)
        self.label.place(**kwargs)


# Testing FrameManager.py
def test():
    if __name__ == "__main__":
        app = MainApp()
        app.geometry("1200x600+350+100")
        app.title("AttendEase App")
        app.mainloop()
