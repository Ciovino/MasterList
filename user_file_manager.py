from secret_stuff import private_folder
import os

# Gestisce la scrittura/lettura/salvataggio dei file privati dell'utente

class UserFileManager:
    def __init__(self, id:int, user_file:list[str]):
        self.user_id = id
        self.active_file = None
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
        self.active_file = new_file_name # Imposta come attivo il file appena creato
        return True

    def save(self, info:str):
        pass

    def get_active_file(self):
        return self.active_file

    def change_active(self, new_active_file: str):
        if new_active_file in self.files:
            self.active_file = new_active_file
            return True
        else:
            return False

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
