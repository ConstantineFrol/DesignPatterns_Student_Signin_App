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
