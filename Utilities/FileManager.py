import json

from Utilities.LogManager import LogManager


class FileManager:

    def __init__(self):
        """Initialize FileManager and create LogManager instance for error logging."""
        self.err_log = LogManager(self.get_path('er_logs'))

    def get_path(self, key_name):

        """Get the file path associated with the given key from the 'paths.json' file."""
        try:
            with open('/home/codewizard/PycharmProjects/DesignPatterns_Student_Signin_App/src/paths.json', 'r') as file:
                json_data = file.read()

            my_dict = json.loads(json_data)

            # Check if the key exists in the dictionary
            if key_name in my_dict:
                # Access and return the value associated with the key
                value = my_dict[key_name]
                return value
            else:
                self.err_log.log_error(f"{self.__class__.__name__}.py - The key '{key_name}' does not exist in the "
                                       f"JSON data.")
        except Exception as e:
            self.err_log.log_error(f"{self.__class__.__name__}.py - {str(e)}")
            return None
