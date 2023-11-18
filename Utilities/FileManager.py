import json

from Utilities.LogManager import LogManager


class FileManager:

    def __init__(self):

        self.log_mngr = LogManager(self.get_path('logs'))

    def get_path(self, key_name):
        try:
            with open('./src/paths.json', 'r') as file:
                json_data = file.read()

            my_dict = json.loads(json_data)

            # Check if the key exists in the dictionary
            if key_name in my_dict:
                # Access and return the value associated with the key
                value = my_dict[key_name]
                return value
            else:
                self.log_mngr.log_error(f"The key '{key_name}' does not exist in the JSON data.")
        except Exception as e:
            self.log_mngr.log_error(f"Error in {self.__class__.__name__}.py:\t{str(e)}")
            return None


# Testing
def test_file_manager():
    file_manager = FileManager()
    key_value = file_manager.get_path('logs')
    print(f"Value for 'logs': {key_value}")

# test_file_manager()
