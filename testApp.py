import os
import shutil
import tkinter as tk
from tkinter import filedialog

import cv2
from PIL import Image, ImageTk


# Define a User class to represent user information
class User:
    def __init__(self, name, email, t_number, image_path, role="student"):
        self.name = name
        self.email = email
        self.t_number = t_number
        self.image_path = image_path
        self.role = role  # Include the 'role' attribute with a default value of "student"

    def __str__(self):
        return (f"User:\nName: {self.name},"
                f"\nEmail: {self.email},"
                f"\nT Number: {self.t_number},"
                f"\nImage Path: {self.image_path},"
                f"\nRole: {self.role}")


# Define the main application view using tkinter
class AppView(tk.Tk):
    def __init__(self, controller):
        super().__init__()

        self.geometry("800x800")  # Set the initial window size to 800x800 pixels
        self.title("Login and Registration App")  # Set the window title

        self.controller = controller  # Store a reference to the controller
        self.current_frame = None  # Initialize the current frame as None

        self.show_login_frame()  # Show the login frame initially

    # Method to show the login frame
    def show_login_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = LoginFrame(self, self.controller)
        self.current_frame.pack(fill="both", expand=True)

    # Method to show the registration frame
    def show_registration_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = RegistrationFrame(self, self.controller)
        self.current_frame.pack(fill="both", expand=True)

    # Method to show the face validity frame (webcam)
    def show_face_validity_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = FaceValidityFrame(self, self.controller)
        self.current_frame.pack(fill="both", expand=True)


# Define the frame for face validity (webcam streaming)
class FaceValidityFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.master = master
        self.controller = controller

        label = tk.Label(self, text="Face Validity")
        label.pack(pady=10)

        back_button = tk.Button(self, text="Back", command=self.master.show_login_frame)
        back_button.pack()

        self.video_capture = None
        self.camera_index = 0

        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack()

        self.try_open_camera()  # Attempt to open the camera

        if self.video_capture is not None:
            self.update()  # Start updating the webcam feed

    def try_open_camera(self):

        try:
            self.video_capture = cv2.VideoCapture(self.camera_index)

            if not self.video_capture.isOpened():
                raise Exception(f"Camera with index {self.camera_index} not available")


        except Exception as e:
            print(e)
            # Switch between camera ports 0 and 1
            # self.camera_index = 1 - self.camera_index
            self.camera_index = self.find_camera_index()
            try:
                self.video_capture = cv2.VideoCapture(self.camera_index)

                if not self.video_capture.isOpened():
                    raise Exception(f"Camera with index {self.camera_index} not available")

            except Exception as e:
                print(e)
                self.video_capture = None

    def update(self):
        if self.video_capture is not None:
            ret, frame = self.video_capture.read()

            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                photo = ImageTk.PhotoImage(Image.fromarray(rgb_frame))

                self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                self.canvas.photo = photo

            self.after(10, self.update)

    def check_camera_in_use(self, index):
        try:
            capture = cv2.VideoCapture(index)

            if capture.isOpened():
                # Check if the camera is in use
                in_use = capture.read()[0]
                capture.release()
                return in_use
            else:
                return False  # Camera not available

        except Exception as e:
            print(f"Error checking camera at index {index}: {e}")
            return False  # An error occurred while checking

    def find_camera_index(self):
        camera_index = 0
        for i in range(10):  # Try indices from 0 to 9
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                print(f"Camera found at index {i}")
                cap.release()
                camera_index = i
        return camera_index


# Define the login frame
class LoginFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.master = master
        self.controller = controller

        label = tk.Label(self, text="Login")  # Create a label
        label.pack(pady=10)  # Pack the label with vertical padding

        sign_in_button = tk.Button(self, text="Sign In", command=self.master.show_face_validity_frame)
        sign_in_button.pack()

        register_button = tk.Button(self, text="Register", command=self.master.show_registration_frame)
        register_button.pack()


# Define the registration frame
class RegistrationFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.master = master
        self.controller = controller

        label = tk.Label(self, text="Registration")
        label.pack(pady=10)

        self.name_label = tk.Label(self, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        self.t_number_label = tk.Label(self, text="T Number:")
        self.t_number_label.pack()
        self.t_number_entry = tk.Entry(self)
        self.t_number_entry.pack()

        # Create a label for the role selection
        role_label = tk.Label(self, text="Select Role:")
        role_label.pack()

        # Create a variable to store the selected role
        self.selected_role = tk.StringVar(self)
        self.selected_role.set("teacher")  # Default role selection

        # Create a dropdown menu for role selection
        role_options = ["teacher", "student"]
        role_dropdown = tk.OptionMenu(self, self.selected_role, *role_options)
        role_dropdown.pack()

        self.icon_label = tk.Label(self, text="Icon", image=None)
        self.icon_label.pack()
        self.icon_label.pack_forget()

        self.small_icon_label = tk.Label(self, text="Small Icon", image=None)
        self.small_icon_label.pack()
        self.small_icon_label.pack_forget()

        upload_button = tk.Button(self, text="Upload Image",
                                  command=self.upload_image)
        upload_button.pack()

        back_button = tk.Button(self, text="Back", command=self.master.show_login_frame)
        back_button.pack()

        register_button = tk.Button(self, text="Register", command=self.register)
        register_button.pack()

    # Method to upload an image for user registration
    def upload_image(self):
        file_path = filedialog.askopenfilename()  # Open a file dialog to select an image
        if file_path:
            self.controller.update_image_path(file_path)  # Update the image path in the controller
            print("File successfully uploaded")
            print("File Path:", file_path)

            # Display the icon in a small size
            self.show_small_icon()

    # Method to display a small-sized icon
    def show_small_icon(self):
        if self.controller.get_image_path():
            icon_image = tk.PhotoImage(file=self.controller.icon_path)  # Load the icon image

            # Resize the icon to a smaller size (e.g., 50x50 pixels)
            small_icon_image = icon_image.subsample(2)  # Adjust the subsample factor as needed

            self.small_icon_label.config(image=small_icon_image)
            self.small_icon_label.image = small_icon_image  # Keep a reference to avoid garbage collection
            self.small_icon_label.pack()  # Show the small icon

    # Method to handle user registration
    def register(self):
        global destination_directory
        name = self.name_entry.get()
        email = self.email_entry.get()
        t_number = self.t_number_entry.get()
        image_path = self.controller.get_image_path()
        role = self.selected_role.get()

        if image_path:
            # Create a User object
            user = User(name, email, t_number, image_path, role)
            print(user)
            print("Registration Successful")

            # Determine the destination directory based on the user's role
            if role == "student":
                destination_directory = "photos/Students"
            elif role == "teacher":
                destination_directory = "photos/Teachers"
            else:
                print("Unknown role, image not copied.")

            # Copy the image to the appropriate directory
            new_image_path = os.path.join(destination_directory, f"{name}.jpg")
            shutil.copy(image_path, new_image_path)
            print(f"Image copied to: {new_image_path}")

            # Clear the form fields and other UI elements
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.t_number_entry.delete(0, tk.END)
            self.controller.update_image_path(None)
            self.small_icon_label.pack_forget()

            # Switch to the Login Frame after a delay (e.g., 2 seconds)
            self.after(2000, self.switch_to_login)

        else:
            print("Please upload an image before registering.")

    # Method to switch to the login frame
    def switch_to_login(self):
        # Call the controller method to switch to the LoginFrame
        self.controller.show_login_frame()


# Define the main application controller
class AppController:
    def __init__(self, icon_path):
        self.user_model = User(name="", email="", t_number="", image_path="")
        self.app_view = AppView(self)  # Create the main application view

        # Icon path
        self.icon_path = icon_path

    # Method to run the application
    def run(self):
        self.app_view.mainloop()

    # Method to update the image path in the user model
    def update_image_path(self, image_path):
        self.user_model.image_path = image_path

    # Method to get the image path from the user model
    def get_image_path(self):
        return self.user_model.image_path

    # Method to show the login frame in the view
    def show_login_frame(self):
        self.app_view.show_login_frame()


if __name__ == "__main__":
    icon_path = 'Images/icons8-ok-48.png'  # Define the path to the application icon
    controller = AppController(icon_path)  # Create the main application controller
    controller.run()  # Run the application
