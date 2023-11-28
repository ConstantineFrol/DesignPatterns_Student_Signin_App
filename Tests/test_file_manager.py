import unittest
from unittest.mock import mock_open, patch
from Utilities.FileManager import FileManager


class TestFileManager(unittest.TestCase):
    def setUp(self):
        # Create a FileManager instance for testing
        self.file_manager = FileManager()

    @patch("builtins.open", new_callable=mock_open, read_data='{"er_logs": "../Logs/error_log.txt"}')
    def test_get_path_existing_key(self, mock_open_file):
        """Tests the case where the key exists in the JSON data."""
        # Test when the key exists in the JSON data
        key_name = 'er_logs'
        key_value = self.file_manager.get_path(key_name)

        # Assert that the mock file was opened
        mock_open_file.assert_called_once_with('../src/paths.json', 'r')

        # Assert that the value returned by get_path is correct
        self.assertEqual(key_value, '../Logs/error_log.txt')

    @patch("builtins.open", side_effect=Exception("File not found"))
    def test_get_path_file_not_found(self, mock_open_file):
        """Tests the case where an exception (file not found) occurs during file reading."""
        # Test when there's an exception (file not found)
        key_name = 'er_logs'
        key_value = self.file_manager.get_path(key_name)

        # Assert that the mock file was opened
        mock_open_file.assert_called_once_with('../src/paths.json', 'r')

        # Assert that the value returned by get_path is None
        self.assertIsNone(key_value)

    @patch("builtins.open", new_callable=mock_open, read_data='{"u_logs": "../Logs/error_log.txt"}')
    def test_get_path_missing_key(self, mock_open_file):
        """Tests the case where the key does not exist in the JSON data."""
        # Test when the key does not exist in the JSON data
        key_name = 'er_logs'
        key_value = self.file_manager.get_path(key_name)

        # Assert that the mock file was opened
        mock_open_file.assert_called_once_with('../src/paths.json', 'r')

        # Assert that the value returned by get_path is None
        self.assertIsNone(key_value)


if __name__ == '__main__':
    unittest.main()
