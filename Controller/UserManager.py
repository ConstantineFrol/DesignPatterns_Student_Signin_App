import cv2
import face_recognition


def encode_img(img):
    encode = face_recognition.face_encodings(img)
    if len(encode) == 0:
        return None
    else:
        return encode[0]


def match_encodings(user_img, encode_list):
    match = face_recognition.compare_faces(encode_list, user_img)
    return match


def start_webcam(self, label):
    if 'cap' not in self.__dict__:
        self.cap = cv2.VideoCapture(0)
        cv2.VideoCapture.set(self.cap, cv2.CAP_PROP_FRAME_WIDTH, 640)

    self._label = label
    self.get_webcam_data()


def get_webcam_data():
    ret, frame = self.cap.read()

    self.img_snap = frame
    current_user_img = cv2.cvtColor(self.img_snap, cv2.COLOR_BGR2RGB)  # if webcam not working - Error
    self.recent_capture = Image.fromarray(current_user_img)
    imgtk = ImageTk.PhotoImage(image=self.recent_capture)
    self._label.imgtk = imgtk
    self._label.configure(image=imgtk)
    # Repeat in 20 seconds
    self._label.after(20, self.get_webcam_data)

