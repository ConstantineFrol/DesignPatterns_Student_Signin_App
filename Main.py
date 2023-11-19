import cv2
import face_recognition
from PIL import Image, ImageTk

from View.FrameManager import MainApp


class App:
    def __init__(self):
        pass

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



    def start(self):
        print("Starting app...")
        app = MainApp()
        app.geometry("1200x600+350+100")
        app.title("AttendEase App")
        app.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
