import unittest
import tempfile
import os

# Import the Database class from your module
from Model.Database import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file for testing
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.db = Database(self.db_path)

    def tearDown(self):
        # Close the database connection and delete the temporary file
        self.db.close_connection()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_insert_and_find_user(self):
        t_number = 't00123456'
        name = 'lol'
        registered = '2023-10-18 23:51:47'
        total_attendance = 5
        role = 'student'
        encode = b'-0.21615925431251526, 0.08906067907810211'

        # Insert a user
        self.db.insert_user(t_number, name, registered, total_attendance, role, encode)

        # Find the user and assert that the retrieved information matches the inserted values
        result = self.db.find_user(t_number)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], t_number)
        self.assertEqual(result[1], name)
        self.assertEqual(result[2], registered)
        self.assertEqual(result[3], total_attendance)
        self.assertEqual(result[4], role)
        self.assertEqual(result[5], encode)

    def test_update_attendance(self):
        t_number = 't00123456'
        new_total_attendance = 10

        # Insert a user
        self.db.insert_user(t_number, 'test_user', '2023-01-01 00:00:00', 5, 'student', b'')

        # Update the attendance for the user
        self.db.update_attendance(t_number, new_total_attendance)

        # Find the user and assert that the attendance has been updated
        result = self.db.find_user(t_number)
        self.assertIsNotNone(result)
        self.assertEqual(result[3], new_total_attendance)


if __name__ == '__main__':
    unittest.main()
