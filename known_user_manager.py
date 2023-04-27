import json
from secret_stuff import private_folder
from user_info import UserInfo

class KnownUserManager:
    def __init__(self, known_user_file:str) -> None:
        self.file_name = private_folder + known_user_file
        self.local_list = KnownUserManager.load_user(self.file_name)

    # New User
    def add_user(self, new_user:UserInfo) -> UserInfo:
        self.local_list.append(new_user)
        self.save_users()
        return new_user
    
    # Check if alredy know the user
    def is_known_user(self, user:UserInfo):
        for saved_user in self.local_list:
            if saved_user.same_user(user):
                return saved_user
        
        return None

    def load_user(file_name) -> list[UserInfo]:
        local_list = []

        # Json file with all the known users
        users_in_file = open(file_name, 'r').readlines()

        entrire_file = ""
        for line in users_in_file:
            entrire_file = entrire_file + (line.replace("\n", '').replace('  ', ''))

        if entrire_file != "":
            all_user = json.loads(entrire_file)
            for user in all_user:
                local_list.append(UserInfo(user['id'], user['name'], "start", user['files']))

        return local_list

    # Save all knwon user in the json file
    def save_users(self) -> None:
        users_in_file = open(self.file_name, 'w')

        json_users = []
        for user in self.local_list:
            json_users.append(user.user_to_table())

        users_in_file.write(json.dumps(json_users, indent=2))

        users_in_file.close()