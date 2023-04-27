import json, os
from secret_stuff import private_folder

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