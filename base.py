import tkinter as tk
from tkinter import filedialog  # Import filedialog module

# Define global variables
current_frame = None
main_frame = None
photo_frame = None
frames = {}
reg_confirm_button = None  # Initialize reg_confirm_button globally
# Define a list to store User objects
user_list = []

# Define a dictionary to store Entry widgets
registration_entries = {}

# Define a StringVar to track the file path
selected_photo_path = tk.StringVar()

root = tk.Tk()
root.title("Registration and Sign In")

# Create the main frame with Register and Sign In buttons
main_frame = create_frame(root, width=800, height=600, text="Welcome To MTU", back_button=False)

# Create the Register frame with the registration form
register_frame = create_frame(root, width=800, height=600, text="Register Form")

# Add the registration form elements to the Register frame
add_registration_form(register_frame)

# Initialize photo_frame as None
photo_frame = None

# Create the Sign In frame
signin_frame = create_frame(root, width=800, height=600, text="Sign In Form")

# Store references to frames in a dictionary


# Create buttons to switch between frames on the main frame
register_button = tk.Button(main_frame, text="Register", command=lambda: show_frame(register_frame))
register_button.pack(pady=20)

signin_button = tk.Button(main_frame, text="Sign In", command=lambda: show_frame(signin_frame))
signin_button.pack(pady=20)

# Store the current active frame (initially main_frame)
current_frame = "main_frame"


def create_frame(root_frame, width, height, text, back_button=True):
    """

    :param root_frame: root
    :param width: width
    :param height: frame height
    :param text: text for label
    :param back_button: default set as visible
    :return: result of the frame
    """
    frames = {
        "main_frame": main_frame,
        "register_frame": register_frame,
        "signin_frame": signin_frame
    }

    frame = tk.Frame(root_frame, width=width, height=height)
    frame.pack_propagate(False)
    frame.pack(fill='both', expand=True)

    # Create Label
    label = tk.Label(frame, text=text)
    label.pack(pady=20)

    if back_button and frame != main_frame:  # Only show the "Back" button if not the main frame
        back_button = tk.Button(frame, text="Back", command=lambda: show_previous_frame())
        back_button.pack(pady=20)

    return frame


def show_frame(frame):
    for key in frames:
        frames[key].pack_forget()
    frame.pack(fill='both', expand=True)


# Function to handle the photo upload
def upload_photo():
    file_path = filedialog.askopenfilename()
    if file_path:
        selected_photo_path.set(file_path)
        check_fields()  # Check fields after photo selection


def add_registration_form(frame):
    # Create form elements and labels
    label_name = tk.Label(frame, text="Name:")
    label_name.pack(pady=5)
    entry_name = tk.Entry(frame)
    entry_name.pack(pady=5)

    label_email = tk.Label(frame, text="Email:")
    label_email.pack(pady=5)
    entry_email = tk.Entry(frame)
    entry_email.pack(pady=5)

    label_student_number = tk.Label(frame, text="Student Number:")
    label_student_number.pack(pady=5)
    entry_student_number = tk.Entry(frame)
    entry_student_number.pack(pady=5)

    # Add an "Add Photo" button to switch to the photo frame
    add_photo_button = tk.Button(frame, text="Add Photo", command=upload_photo)
    add_photo_button.pack(pady=10)

    # Create a StringVar to track the file path
    selected_photo_path = tk.StringVar()

    # Add a "Register" button with the initial state set to 'disabled'
    reg_confirm_button = tk.Button(register_frame, text="Register",
                                   command=lambda: register_user(selected_photo_path.get()), state='disabled')
    reg_confirm_button.pack(pady=10)

    # Bind the check_fields function to the Entry widgets and selected photo path
    registration_entries["name"].bind("<FocusOut>",
                                      lambda event: check_fields(register_frame, reg_confirm_button,
                                                                 registration_entries,
                                                                 selected_photo_path))
    registration_entries["email"].bind("<FocusOut>",
                                       lambda event: check_fields(register_frame, reg_confirm_button,
                                                                  registration_entries,
                                                                  selected_photo_path))
    registration_entries["student_number"].bind("<FocusOut>",
                                                lambda event: check_fields(register_frame, reg_confirm_button,
                                                                           registration_entries,
                                                                           selected_photo_path))
    selected_photo_path.trace_add("write",
                                  lambda *args: check_fields(register_frame, reg_confirm_button, registration_entries,
                                                             selected_photo_path))

    # Add a "Register" button
    reg_confirm_button = tk.Button(register_frame, text="Register",
                                   command=lambda: register_user(register_frame, selected_photo_path.get()),
                                   state='disabled')

    reg_confirm_button.pack(pady=10)

    # Store the Entry widgets in a dictionary for later access
    registration_entries["name"] = entry_name
    registration_entries["email"] = entry_email
    registration_entries["student_number"] = entry_student_number


# Create a function to check fields and enable/disable the "Register" button
def check_fields(frame, user_function, entries, photo_path_var):
    name = entries["name"].get()
    email = entries["email"].get()
    student_number = entries["student_number"].get()

    # Check if all fields are not empty and a photo is selected
    if name and email and student_number and photo_path_var.get():
        user_function.config(state='normal')  # Enable the button
    else:
        user_function.config(state='disabled')  # Disable the button


def show_photo_frame():
    global photo_frame
    if photo_frame is not None:
        photo_frame.destroy()  # Destroy the current photo frame if it exists

    # Create a new frame for adding a photo as a child of the current active frame
    photo_frame = create_frame(frames[current_frame], width=800, height=600, text="Add Photo", back_button=True)

    # Add buttons to the photo frame
    back_button = tk.Button(photo_frame, text="Back", command=show_previous_frame)
    back_button.pack(pady=10)

    make_photo_button = tk.Button(photo_frame, text="Make Photo", command=make_photo)
    make_photo_button.pack(pady=10)

    cancel_button = tk.Button(photo_frame, text="Cancel", command=show_main_frame)
    cancel_button.pack(pady=10)

    # Show the new frame for adding a photo
    show_frame(photo_frame)


def show_previous_frame():
    show_frame(frames[current_frame])


def show_main_frame():
    show_frame(main_frame)


def make_photo():
    # Implement logic to take a photo here
    pass


# Function to create a User object when the "Register" button is pressed
def register_user(register_frame, photo_path):
    # Get values from tkinter Entry widgets
    name = registration_entries["name"].get()
    email = registration_entries["email"].get()
    student_number = registration_entries["student_number"].get()


# Define a User class
class User:
    def __init__(self, name, email, student_number, photo_path):
        self.name = name
        self.email = email
        self.student_number = student_number
        self.photo_path = photo_path  # Store the photo path in the User object


# Function to create a User object when the "Register" button is pressed
def register_user():
    # Get values from tkinter Entry widgets
    name = registration_entries["name"].get()
    email = registration_entries["email"].get()
    student_number = registration_entries["student_number"].get()

    # Get the selected photo path
    photo_path = selected_photo_path.get()

    # Check if the selected photo path is not empty
    if not photo_path:
        # Handle the case where no photo is selected
        print("Please select a photo before registering.")
        return

    # Create a new User object with the photo path
    new_user = User(name, email, student_number, photo_path)

    # You can now use the 'new_user' object as needed
    # For example, you can store it in a list or perform further processing
    user_list.append(new_user)

    # Optionally, print the user's information
    print("New User:")
    print("Name:", new_user.name)
    print("Email:", new_user.email)
    print("Student Number:", new_user.student_number)
    print("Photo Path:", new_user.photo_path)  # Print the photo path


show_frame(main_frame)  # Show the main frame initially

root.mainloop()
