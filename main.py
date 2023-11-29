import cv2
import face_recognition
from PIL import Image, ImageTk

from View.FrameManager import MainApp


class App:

    def start(self):
        print("Starting App...")
        my_app = MainApp()
        my_app.geometry("1200x600+350+100")
        my_app.title("AttendEase App")
        my_app.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
