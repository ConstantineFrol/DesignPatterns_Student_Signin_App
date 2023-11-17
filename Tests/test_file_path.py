import os


def check_directory_and_file(directory_path, file_name):
    # Check if the directory exists
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        print(f"The directory '{directory_path}' exists.")

        # Construct the full path to the file
        file_path = os.path.join(directory_path, file_name)

        # Check if the file exists
        if os.path.exists(file_path) and os.path.isfile(file_path):
            print(f"The file '{file_name}' is found in the directory.")
        else:
            print(f"The file '{file_name}' does not exist in the directory.")
    else:
        print(f"The directory '{directory_path}' does not exist.")


# Example usage
directory_path = '../DB_Sqlite3'
file_name = 'mtu.db'
check_directory_and_file(directory_path, file_name)
