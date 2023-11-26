from datetime import datetime


def _get_registration_date():
    """Get the formatted current date and time as a string."""
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


class User:
    def __init__(self, user_id, user_name, attendance_qty, user_role, img_encode):
        """Initialize a User with the provided information."""
        self.t_number = user_id
        self.name = user_name
        self.registration_date = _get_registration_date()
        self.total_attendance = attendance_qty
        self.role = user_role
        self.encode = img_encode

    def get_t_number(self):
        """Get the T number of the user."""
        return self.t_number

    def get_name(self):
        """Get the name of the user."""
        return self.name

    def get_registration_date(self):
        """Get the registration date of the user."""
        return self.registration_date

    def get_total_attendance(self):
        """Get the total attendance of the user."""
        return self.total_attendance

    def get_role(self):
        """Get the role of the user."""
        return self.role

    def get_encode(self):
        """Get the image encoding of the user."""
        return self.encode

    def __str__(self):
        """String representation of the User object."""
        return f"User Info:\n\
                t_number: {self.t_number}\n\
                name: {self.name}\n\
                registered: {self.registration_date}\n\
                total_attendance: {self.total_attendance}\n\
                role: {self.role}\n\
                encode: {self.encode}"


# Test
def test_user():
    """Test the functionality of the User class."""
    t_number = 't00123456'
    name = 'lol'
    total_attendance = 5
    role = 'student'
    encode = '-0.21615925431251526, 0.08906067907810211, ...'  # (truncated for brevity)

    user = User(t_number, name, total_attendance, role, encode)

    # Print user information
    print(user)
