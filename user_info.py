import json, os
from secret_stuff import private_folder

class KnownUserManager:
    def __init__(self, known_user_file:str) -> None:
        self.file_name = private_folder + known_user_file
        self.local_list = KnownUserManager.load_user(self.file_name)

    # New User
    def add_user(self, new_user) -> None:
        self.local_list.append(new_user)
        self.save_users()
    
    # Check if alredy know the user
    def is_known_user(self, user):
        for saved_user in self.local_list:
            if saved_user.same_user(user):
                return saved_user
        
        return None

    def load_user(file_name) -> list:
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

class UserInfo:
    def __init__(self, id:int, name:str, state, files:list) -> None:
        self.id = id
        self.name = name
        self.state = state
        self.files = files

    # Check if self and other are the same user
    def same_user(self, other) -> bool:
        if type(other) is int:
            return self.id == other
        else:
            return self.id == other.id

    def add_file(self, user_file_name:str):
        # Check if the private user directory exists
        if not os.path.exists(self.get_user_folder()):
            os.mkdir(self.get_user_folder())
        
        # Check if file already exists
        if self.is_file(user_file_name):
            # Cannot create file
            return False
        
        file_opened = open(self.get_complete_file_name(user_file_name), "w")
        file_opened.write(user_file_name)
        file_opened.close()

        self.files.append(user_file_name)

        return True

    def is_file(self, file_name:str) -> bool:
        file_name = file_name.replace(' ', '_').lower()

        for saved_file in self.files:
            if (saved_file.replace(' ', '_').lower()) == file_name:
                return True
            
        return False

    def get_user_folder(self) -> str:
        return f'{private_folder}{self.id}'
    
    def get_complete_file_name(self, user_file_name) -> str:
        correct_file_name = user_file_name.replace(' ', '_').lower()

        return f'{self.get_user_folder()}\\{correct_file_name}.json'

    # Create a dictionary
    def user_to_table(self) -> dict:
        return { 
            'id': self.id, 
            'name': self.name,
            'files' : self.files
        }

    # Json string
    def user_to_json(self) -> str:
        return json.dumps(self.user_to_table())