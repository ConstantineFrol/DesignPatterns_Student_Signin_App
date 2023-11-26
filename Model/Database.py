import sqlite3


class Database:
    def __init__(self, db_name):
        """Initialize the Database with the given name and create the 'users' table if it doesn't exist."""
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Create the users table if it doesn't exist
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS users (t_number TEXT, name TEXT, registered TEXT, total_attendance INTEGER, role TEXT, encode BLOB)')

    def insert_user(self, t_number, name, registered, total_attendance, role, encode):
        """Insert a new user into the 'users' table."""
        self.cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)',
                            (t_number, name, registered, total_attendance, role, sqlite3.Binary(encode)))
        self.conn.commit()

    def find_user(self, t_number):
        """Find a user in the 'users' table based on their T number."""
        self.cursor.execute('SELECT * FROM users WHERE t_number=?', (t_number,))
        result = self.cursor.fetchone()
        return result

    def print_all_users(self):
        """Print all users in the 'users' table."""
        for row in self.cursor.execute('SELECT * FROM users'):
            print(row)

    def get_all_users_encode(self):
        """Retrieve T numbers and encodings of all users from the 'users' table."""
        self.cursor.execute('SELECT t_number, encode FROM users')
        result = self.cursor.fetchall()
        return result

    def update_attendance(self, t_number, new_total_attendance):
        """Update the 'total_attendance' value for a user in the 'users' table."""
        self.cursor.execute('UPDATE users SET total_attendance=? WHERE t_number=?',
                            (new_total_attendance, t_number))
        self.conn.commit()

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()

    def delete_user(self, t_number):
        """Delete a user from the 'users' table based on their T number."""
        self.cursor.execute("DELETE FROM users WHERE t_number=?", (t_number,))


# # Testing of Usage
# def test_db():
#     """Test the functionality of the Database class."""
#     db = Database('../DB_Sqlite3/mtu.db')
#
#     t_number = 't00123456'
#     name = 'lol'
#     registered = '2023-10-18 23:51:47'
#     total_attendance = 5
#     role = 'student'
#     encode = '-0.21615925431251526, 0.08906067907810211, ...'  # (truncated for brevity)
#
#     db.cursor.execute(f'DELETE FROM users')
#
#     # db.insert_user(t_number, name, registered, total_attendance, role, encode)
#
#     db.print_all_users()
#     print(f'Result: {db.find_user(t_number)}')
#     db.delete_user(t_number)
#     # print('All users\n', db.print_all_users())
#     # Close the connection when done
#     db.close_connection()
#
#
# def test_db_2():
#     """Another test function to demonstrate the usage of Database class."""
#     db = Database('../DB_Sqlite3/mtu.db')
#
#     all_users_encode = db.get_all_users_encode()
#     print(f'All users encode type: {type(all_users_encode)}')
#     for user_info in all_users_encode:
#         t_number, encode = user_info
#         print(f'T_number: {t_number}, Encode: {encode}')
#
#     # Close the connection when done
#     db.close_connection()
#
#
# def delete_all_users():
#     """Delete all users from the 'users' table."""
#     db = Database('../DB_Sqlite3/mtu.db')
#     db.cursor.execute(f'DELETE FROM users')
#     db.close_connection()
#
# # test_db()
# # test_db_2()
# # delete_all_users()
