from secret_stuff import private_folder
import os, json
from utility import get_json_string

# Gestisce la scrittura/lettura/salvataggio dei file privati dell'utente

class UserFileManager:
    def __init__(self, id:int, user_file:list[str]):
        self.user_id = id
        self.active_file = None
        self.loaded_file : list[str] = []
        self.files = user_file
    
    def add_file(self, new_file_name:str) -> bool:
        # Controlla che esista la cartella dell'utente
        if not os.path.exists(self.get_user_folder()):
            os.mkdir(self.get_user_folder())
        
        # Crea il file
        try:
            open(self.get_complete_file_name(new_file_name), 'x').close()
        except FileExistsError: # Il file non esiste
            return False

        self.files.append(new_file_name)
        self.change_active(new_file_name) # Imposta come attivo il file appena creato
        return True

    def save(self, info:str):
        self.loaded_file.append(info)
        self.save_on_file(self.active_file)

    def show(self) -> list[str]:
        return self.loaded_file

    def delete(self, file_to_delete:str):
        if not self.is_file(file_to_delete):
            return False
        
        if file_to_delete == self.active_file:
            self.active_file = None
            self.loaded_file = []

        if os.path.exists(self.get_complete_file_name(file_to_delete)):
            os.remove(self.get_complete_file_name(file_to_delete))
        else:
            return False
        
        self.files.remove(file_to_delete)

        return True

    def get_active_file(self):
        return self.active_file

    def change_active(self, new_active_file: str):
        if new_active_file in self.files:
            self.save_on_file(self.active_file)

            self.active_file = new_active_file
            self.loaded_file = []

            self.load_file(new_active_file)

            return True
        else:
            return False

    def save_on_file(self, to_file:str):
        if to_file == None:
            return

        open_file = open(self.get_complete_file_name(to_file), 'w')

        json_strings = []

        for phrase in self.loaded_file:
            tmp = {'value': phrase}
            json_strings.append(tmp)
        
        open_file.write(json.dumps(json_strings, indent=2))
        
        open_file.close()

    def load_file(self, from_file: str):
        phrases = get_json_string(self.get_complete_file_name(from_file))

        for phrase in phrases:
            self.loaded_file.append(phrase['value'])

    def get_files(self) -> list[str]:
        return self.files

    def get_user_folder(self) -> str:
        return f'{private_folder}{self.user_id}'
    
    def is_file(self, file_name:str) -> bool:
        file_name = file_name.replace(' ', '_').lower()

        for saved_file in self.files:
            if (saved_file.replace(' ', '_').lower()) == file_name:
                return True
            
        return False
    
    def get_complete_file_name(self, user_file_name) -> str:
        correct_file_name = user_file_name.replace(' ', '_').lower()
        return f'{self.get_user_folder()}\\{correct_file_name}.json'
