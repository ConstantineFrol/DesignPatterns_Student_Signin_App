import numpy as np
from Model.Database import Database
from Utilities.FileManager import FileManager
from Utilities.LogManager import LogManager

class DatabaseManager:
    _instance = None

    def __new__(cls):
        """Singleton implementation to ensure only one instance is created."""
        if not cls._instance:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the DatabaseManager."""
        if self._initialized:
            return

        # Initialize dependencies
        self.file_manager = FileManager()
        self.db_path = self.file_manager.get_path('db')
        self.db = Database(self.db_path)
        self.error_log = LogManager(self.file_manager.get_path('er_logs'))
        self._initialized = True

    def insert_user(self, user):
        """Insert a user into the database."""
        try:
            self.db.insert_user(user.get_t_number(), user.get_name(), user.get_registration_date(),
                                user.get_total_attendance(), user.get_role(), user.get_encode())
        except Exception as e:
            self.error_log.log_error(f"Error inserting user: {str(e)}")

    def find_user(self, t_number):
        """Find a user in the database by their T number."""
        try:
            if t_number is None:
                return None
            else:
                return self.db.find_user(t_number)
        except Exception as e:
            self.error_log.log_error(f"Error finding user: {str(e)}")
            return None

    def get_name_with_t_no(self, t_number):
        """Get the name of a user based on their T number."""
        results = self.find_user(t_number)
        if results:
            return results[1]
        else:
            return None

    def print_all_users(self):
        """Print all users in the database."""
        try:
            users = self.db.print_all_users()
            if users:
                return users
            else:
                return None
        except Exception as e:
            self.error_log.log_error(f"Error printing all users: {str(e)}")
            return None

    def get_all_users_encode(self):
        """Get the encoding of all users in the database."""
        try:
            all_users_encode = self.db.get_all_users_encode()
            if all_users_encode:
                return all_users_encode
            else:
                return None
        except Exception as e:
            self.error_log.log_error(f"Error getting all users' encode: {str(e)}")
        return None

    def close_connection(self):
        """Close the database connection."""
        try:
            self.db.close_connection()
        except Exception as e:
            self.error_log.log_error(f"Error closing database connection: {str(e)}")

    def get_usr_encod_as_arr(self):
        """Get user encodings as NumPy arrays."""
        all_users_encode = self.db.get_all_users_encode()

        if not all_users_encode:
            return None

        all_users_arrays = []

        for user_encode_tuple in all_users_encode:
            user_t_number, sample_bytes = user_encode_tuple

            dtype = np.float64
            shape = (128,)

            # Convert the bytes to a NumPy array
            user_encode_array = np.frombuffer(sample_bytes, dtype=dtype).reshape(shape)

            all_users_arrays.append((user_t_number, user_encode_array))

        return all_users_arrays

    def modify_attendance(self, t_number, attendance_change=1):
        """Modify the attendance of a user."""
        # Find the user first
        user = self.find_user(t_number)
        if user:
            try:
                current_total_attendance = int(user[3])
                new_total_attendance = current_total_attendance + attendance_change

                self.db.update_attendance(t_number, new_total_attendance)
            except Exception as e:
                self.error_log.log_error(f"Error modifying attendance: {str(e)}")