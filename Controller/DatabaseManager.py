from Utilities.FileManager import FileManager
from Model.UserDatabase import UserDatabase


class DatabaseManager:
    def __init__(self, db_name):
        self.db = UserDatabase('mtu.db')

        self.file_manager = FileManager("error_log.txt")

    def insert_user(self, user):
        try:
            self.db.insert_user(user.get_t_number(), user.get_name(), user.get_registration_date(),
                                user.get_total_attendance(), user.get_role(), user.get_encode())
            self.file_manager.log_info("User inserted successfully.")
        except Exception as e:
            self.file_manager.log_error(f"Error inserting user: {str(e)}")

    def find_user(self, t_number):
        try:
            if t_number is None:
                return None
            else:
                return self.db.find_user(t_number)
        except Exception as e:
            self.file_manager.log_error(f"Error finding user: {str(e)}")
            return None

    def print_all_users(self):
        try:
            users = self.db.print_all_users()
            if users:
                return users
            else:
                return None
        except Exception as e:
            self.file_manager.log_error(f"Error printing all users: {str(e)}")
            return None

    def close_connection(self):
        try:
            self.db.close_connection()
            self.file_manager.log_info("Database connection closed.")
        except Exception as e:
            self.file_manager.log_error(f"Error closing database connection: {str(e)}")
