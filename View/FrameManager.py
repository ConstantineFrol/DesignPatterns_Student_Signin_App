import tkinter as tk

from Controller.UserManager import UserManager
from Utilities.FileManager import FileManager
from Utilities.LogManager import LogManager
from View.UIManager import UIManager


class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Create a container to hold the frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # Dictionary to hold different frames

        # Create and add frames to the dictionary
        for F in (MainFrame, RegistrationFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the initial frame
        self.show_frame(MainFrame)

    def show_frame(self, cont):
        # Raise the requested frame to the top
        frame = self.frames[cont]
        frame.tkraise()


class MainFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.main_window = UIManager()

        self.login_btn = self.main_window.create_btn(self, 'login', 'green', self.login)
        self.login_btn.place(x=850, y=200)

        self.logout_btn = self.main_window.create_btn(self, 'Logout', 'red', self.logout)
        self.logout_btn.place(x=850, y=300)

        self.registration_btn = self.main_window.create_btn(self, 'Register New User', 'gray',
                                                            command=lambda: controller.show_frame(RegistrationFrame),
                                                            fg='black')
        self.registration_btn.place(x=850, y=400)

        self.camera_label = self.main_window.create_label(self)
        self.camera_label.place(x=20, y=20, width=750, height=500)

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


class RegistrationFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.file_manager = FileManager()
        self.log_mngr = LogManager(self.file_manager.get_path('logs'))
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
        user_name = self.user_name_input.get(1.0, "end-1c").strip()
        user_role = self.user_role_input.get(1.0, "end-1c").strip()
        user_t_num = self.user_id_input.get(1.0, "end-1c").strip()
        # user_img_encode = face_recognition.face_encodings(self.new_user_capture)[0]
        user_img_encode = '0, 0,'  # temporary

        usr_mngr = UserManager()
        if usr_mngr.register_new_user(user_t_num, user_name, 0, user_role, user_img_encode):

            self.controller.show_frame(MainFrame)
            self.reg_window.msg_box('Success!', f'{user_name} has successfully registered !')
        else:
            self.log_mngr.log_error(f'Error registering user: {str(user_name)}')
            self.reg_window.msg_box(f'Error', 'Error registering user.')
        # user_img_encode = face_recognition.face_encodings(self.new_user_capture)[0]
        #
        # file = open(os.path.join(self.db_dir, '{}.pickle'.format(user_name)), 'wb')
        # pickle.dump(user_img_encode, file)
        # self.registration_window.destroy()

    def add_label(self, text, font_size, **kwargs):
        self.label = self.reg_window.get_text_label(self, text, font_size)
        self.label.place(**kwargs)


# Testing FrameManager.py
def test():
    if __name__ == "__main__":
        app = MainApp()
        app.geometry("1200x600+350+100")
        app.title("AttendEase App")
        app.mainloop()
