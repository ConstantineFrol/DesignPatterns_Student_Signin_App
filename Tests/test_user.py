import unittest

from Model.User import User


class TestUser(unittest.TestCase):

    def test_user_creation(self):
        self.maxDiff = None  # To see the full string representation of the user object

        # Test
        t_number = 't00123456'
        name = 'John Doe'
        total_attendance = 5
        role = 'student'
        encode = '-0.21615925431251526, 0.08906067907810211'

        # Act
        user = User(t_number, name, total_attendance, role, encode)
        registration_date = user.get_registration_date()

        # Assert
        self.assertEqual(user.get_t_number(), t_number)
        self.assertEqual(user.get_name(), name)
        self.assertEqual(user.get_total_attendance(), total_attendance)
        self.assertEqual(user.get_role(), role)
        self.assertEqual(user.get_encode(), encode)
        self.assertEqual(user.get_registration_date(), registration_date)

    def test_user_str_representation(self):
        self.maxDiff = None  # To see the full string representation of the user object

        # Arrange
        t_number = 't00123456'
        name = 'John Doe'
        total_attendance = 5
        role = 'student'
        encode = '-0.21615925431251526, 0.08906067907810211'

        # Act
        user = User(t_number, name, total_attendance, role, encode)

        # Assert statements to check the string representation
        expected_str = f"User Info:\n\
                            t_number: {t_number}\n\
                            name: {name}\n\
                            registered: {user.get_registration_date()}\n\
                            total_attendance: {total_attendance}\n\
                            role: {role}\n\
                            encode: {encode}"
        self.assertEqual(str(user), expected_str)


if __name__ == '__main__':
    unittest.main()
