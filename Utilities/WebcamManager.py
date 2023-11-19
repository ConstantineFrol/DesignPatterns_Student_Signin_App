import cv2
import numpy as np
from PIL import Image, ImageTk

from Utilities.FileManager import FileManager
from Utilities.LogManager import LogManager


class WebcamManager:

    def __init__(self):
        self.file_manager = FileManager()
        self.file_manager = LogManager(f'./{self.file_manager.get_path("logs")}')

    def start_webcam(self, label, camera_index):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(camera_index)
            cv2.VideoCapture.set(self.cap, cv2.CAP_PROP_FRAME_WIDTH, 640)

        self.snap = label
        self.get_webcam_data()

    def get_webcam_data(self):
        ret, frame = self.cap.read()

        if not ret:
            error_message = "Failed to read from the webcam."
            # self.file_manager.log_error(str(f'{error_message} in {self.__class__.__name__}.py'))
            # self.file_manager.log_error('Failed to read from the webcam.')
            return None
        else:
            self.img_snap = frame
            current_user_img = cv2.cvtColor(self.img_snap, cv2.COLOR_BGR2RGB)
            self.recent_capture = Image.fromarray(current_user_img)
            imgtk = ImageTk.PhotoImage(image=self.recent_capture)
            self.snap.imgtk = imgtk
            self.snap.configure(image=imgtk)
            # Repeat in 20 seconds
            self.snap.after(20, self.get_webcam_data)

    def get_user_snap(self):
        if self.img_snap is not None:
            return self.img_snap
        else:
            print("Error: Unable to create PhotoImage. img_snap is None.")
            return None

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.recent_capture)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        # self.new_user_capture = self.img_snap.copy()

    def get_user_img(self):
        if self.recent_capture:
            imgtk = ImageTk.PhotoImage(image=self.recent_capture)
            return imgtk
        else:
            print("Error: Unable to create PhotoImage. recent_capture is None.")
            return None


