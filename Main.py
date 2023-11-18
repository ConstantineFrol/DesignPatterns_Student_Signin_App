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

    def register_new_user(self):
        print('New user registered')

    def recognize_user(img, db_connection):

        embeddings_unknown = face_recognition.face_encodings(img)
        if len(embeddings_unknown) == 0:
            return 'no_persons_found'

        embeddings_unknown = embeddings_unknown[0]

        all_users_encode = db_connection.get_all_users_encode()

        match = False
        user_id = 'unknown_person'

        for t_number, encode in all_users_encode:
            match = face_recognition.compare_faces([encode], embeddings_unknown)[0]
            if match:
                user_id = t_number
                break

        return user_id

    def start(self):
        print("Starting app...")
        app = MainApp()
        app.geometry("1200x600+350+100")
        app.title("AttendEase App")
        app.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
