import cv2
import face_recognition
from PIL import Image, ImageTk

from View.FrameManager import MainApp


class App:

    def start(self):
        print("Starting app...")
        app = MainApp()
        app.geometry("1200x600+350+100")
        app.title("AttendEase App")
        app.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
