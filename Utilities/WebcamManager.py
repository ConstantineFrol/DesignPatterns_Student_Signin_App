import cv2
from PIL import Image, ImageTk

from Utilities.FileManager import FileManager
from Utilities.LogManager import LogManager


class WebcamManager:
    _instance = None  # Class variable to store the instance

    def __new__(cls):
        """Singleton pattern: Create a single instance of WebcamManager."""
        if cls._instance is None:
            cls._instance = super(WebcamManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize WebcamManager and set up instance variables."""
        if self._initialized:
            return
        self._initialized = True

        self.file_manager = FileManager()
        self.log_manager = LogManager(f'./{self.file_manager.get_path("er_logs")}')

        self.cap = None
        self.snap = None
        self.img_snap = None
        self.recent_capture = None

    def start_webcam(self, label, camera_index):
        """
        Start the webcam and set up the label for displaying the video stream.

        Parameters:
        - label: The label where the video stream will be displayed.
        - camera_index: The index of the camera to use.
        """
        if self.cap is None:
            self.cap = cv2.VideoCapture(camera_index)
            cv2.VideoCapture.set(self.cap, cv2.CAP_PROP_FRAME_WIDTH, 640)

        self.snap = label
        self.get_webcam_data()

    def get_webcam_data(self):
        """Read a frame from the webcam, convert it to an ImageTk format, and update the label."""
        ret, frame = self.cap.read()

        if not ret:
            error_message = "Failed to read from the webcam."
            self.log_manager.log_error(str(f'{error_message} in {self.__class__.__name__}.py'))
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
        """Get the current snapshot from the webcam."""
        if self.img_snap is not None:
            return self.img_snap
        else:
            print("Error: Unable to create PhotoImage. img_snap is None.")
            return None

    def add_img_to_label(self, label):
        """Add the recent capture image to the specified label."""
        imgtk = ImageTk.PhotoImage(image=self.recent_capture)
        label.imgtk = imgtk
        label.configure(image=imgtk)

    def get_user_img(self):
        """Get the recent capture image in ImageTk format."""
        if self.recent_capture:
            imgtk = ImageTk.PhotoImage(image=self.recent_capture)
            return imgtk
        else:
            print("Error: Unable to create PhotoImage. recent_capture is None.")
            return None
