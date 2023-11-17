import cv2
from PIL import Image, ImageTk

from Utilities.FileManager import FileManager


class WebcamManager:

    def __init__(self, camera_index):
        self.camera_index = camera_index
        self.cap = None
        self.img_snap = None
        self.file_manager = FileManager("error_log.txt")

    def start_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
            cv2.VideoCapture.set(self.cap, cv2.CAP_PROP_FRAME_WIDTH, 640)

        self._label = label
        self.get_webcam_data()

    def get_webcam_data(self):
        ret, frame = self.cap.read()

        if not ret:
            error_message = "Failed to read from the webcam."
            self.file_manager.log_error(error_message)
            return None
        else:
            self.img_snap = frame
            current_user_img = cv2.cvtColor(self.img_snap, cv2.COLOR_BGR2RGB)  # if webcam not working - Error
            self.recent_capture = Image.fromarray(current_user_img)
            imgtk = ImageTk.PhotoImage(image=self.recent_capture)
            self._label.imgtk = imgtk
            self._label.configure(image=imgtk)
            # Repeat in 20 seconds
            self._label.after(20, self.get_webcam_data)
