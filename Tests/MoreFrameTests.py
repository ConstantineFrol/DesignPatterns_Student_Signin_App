import tkinter as tk

from View.UIManager import UIManager


class MainApplication(tk.Tk):
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
        label = tk.Label(self, text="Frame 2", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

        # Button to switch to Frame 1
        button = tk.Button(self, text="Switch to Frame 1",
                           command=lambda: controller.show_frame(MainFrame))
        button.pack()


if __name__ == "__main__":
    app = MainApplication()
    app.geometry("1200x600+350+100")
    app.title("Frame Switching Example")
    app.mainloop()
