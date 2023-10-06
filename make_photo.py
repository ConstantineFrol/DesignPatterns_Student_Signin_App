import cv2
import os

# Load the Haar Cascade Classifier for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

index = 0

for i in range(10):  # Try indices from 0 to 9
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera found at index {i}")
        index = i
        cap.release()

# Initialize the camera using the correct index
cap = cv2.VideoCapture(index)  # Use index 0 for /dev/video0

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    capturing = False
    frame_count = 0
    photos_folder = "photos"

    # Create the photos folder if it doesn't exist
    if not os.path.exists(photos_folder):
        os.makedirs(photos_folder)

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        if ret:
            # Convert the frame to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the grayscale frame
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

            # Detect eyes within each face rectangle
            for (x, y, w, h) in faces:
                # Define the region of interest (ROI) for eye detection
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]

                # Detect eyes in the ROI
                eyes = eye_cascade.detectMultiScale(roi_gray)

                # If two red frames (eyes) are detected inside the green frame (face), capture and save the content
                if len(eyes) == 2:
                    frame_count += 1
                    if frame_count >= 10:  # Capture after 10 consecutive frames with two eyes
                        # Crop the ROI without drawing rectangles around eyes
                        roi_to_save = roi_color.copy()
                        photo_filename = os.path.join(photos_folder, f"captured_image_{frame_count}.jpg")
                        cv2.imwrite(photo_filename, roi_to_save)
                        print(f"Image captured and saved as '{photo_filename}'")
                        capturing = True
                        frame_count = 0

            cv2.imshow("Press 'p' to Capture", frame)

            # Check for key presses
            key = cv2.waitKey(1) & 0xFF

            # Press 'q' to exit the loop
            if key == 113:
                break

            # Clear the frame if a photo has been captured
            if capturing:
                frame_count = 0
                break  # Immediately exit the loop after capturing

        else:
            print("Error: Could not capture a frame from the camera.")

    # Release the camera immediately after capturing
    cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
