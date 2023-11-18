from Controller.DatabaseManager import DatabaseManager
from Model.User import User


class UserManager:
    def __init__(self):
        self.db_mgmt = None
        self.db_connection = DatabaseManager()

    def recognize_user(self, img_snap, db_connection):
        pass

    def login(self):
        # t_number = self.recognize_user(self.img_snap, self.db_connection)
        #
        # if t_number in ['unknown_person', 'no_persons_found']:
        #     self.main_window.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
        # else:
        #     user_info = self.db_connection.find_user(t_number)
        #     if user_info:
        #         name = user_info['name']
        #         self.main_window.msg_box('Welcome back !', f'Welcome, {name}.')
        #         with open(self.log_path, 'a') as f:
        #             f.write(f'{name},{datetime.now()},in\n')
        #     else:
        #         self.main_window.msg_box('Error', 'User information not found.')

        print('You just logged in')

    def logout(self):
        # name = util.recognize(self.img_snap, self.db_dir)
        #
        # if name in ['unknown_person', 'no_persons_found']:
        #     self.main_window.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
        # else:
        #     user_info = self.db_connection.find_user_by_name(name)
        #     if user_info:
        #         self.main_window.msg_box('See you soon!', f'Goodbye, {name}.')
        #         with open(self.lgn_det_path, 'a') as f:
        #             f.write(f'{name},{datetime.now()},out\n')
        #     else:
        #         self.main_window.msg_box('Error', 'User information not found.')

        print('You just logged out')

    def register_new_user(self, user_t_num, user_name, attendance_qty, user_role, user_img_encode):
        user = User(str(user_t_num).lower(), str(user_name).lower(), attendance_qty, str(user_role).lower(), user_img_encode)
        self.db_mgmt = DatabaseManager()
        self.db_mgmt.insert_user(user)
        # check if user was created
        if self.db_mgmt.find_user(user_t_num) is not None:
            self.db_mgmt.close_connection()
            return True
        else:
            self.db_mgmt.close_connection()
            return False