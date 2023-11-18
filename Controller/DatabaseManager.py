from Model.Database import Database
from Utilities.LogManager import LogManager


class DatabaseManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        # Your initialization code here
        self.db = Database('./DB_Sqlite3/mtu.db')
        self.log_mngr = LogManager("Logs/error_log.txt")
        self._initialized = True

    def insert_user(self, user):
        try:
            self.db.insert_user(user.get_t_number(), user.get_name(), user.get_registration_date(),
                                user.get_total_attendance(), user.get_role(), user.get_encode())
            self.log_mngr.log_info("User inserted successfully.")
        except Exception as e:
            self.log_mngr.log_error(f"Error inserting user: {str(e)}")

    def find_user(self, t_number):
        try:
            if t_number is None:
                return None
            else:
                return self.db.find_user(t_number)
        except Exception as e:
            self.log_mngr.log_error(f"Error finding user: {str(e)}")
            return None

    def print_all_users(self):
        try:
            users = self.db.print_all_users()
            if users:
                return users
            else:
                return None
        except Exception as e:
            self.log_mngr.log_error(f"Error printing all users: {str(e)}")
            return None

    def get_all_users_encode(self):
        try:
            all_users_encode = self.db.get_all_users_encode()
            if all_users_encode:
                return all_users_encode
            else:
                return None
        except Exception as e:
            self.log_mngr.log_error(f"Error getting all users' encode: {str(e)}")
            return None

    def close_connection(self):
        try:
            self.db.close_connection()
            self.log_mngr.log_info("Database connection closed.")
        except Exception as e:
            self.log_mngr.log_error(f"Error closing database connection: {str(e)}")


