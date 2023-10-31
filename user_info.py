import json, os
from user_file_manager import UserFileManager

# Racchiude tutte le informazioni di un utente

class UserInfo:
    def __init__(self, id:int, name:str, state, files:list) -> None:
        self.id = id
        self.name = name
        self.state = state

        self.file_manager = UserFileManager(id, files)

    # Controlla se è lo stesso utente
    def same_user(self, other) -> bool:
        if type(other) is int:
            return self.id == other
        else:
            return self.id == other.id

    # Aggiungi un nuovo file
    def add_file(self, user_file_name:str):
        return self.file_manager.add_file(user_file_name)
    
    # Recupera i l nome del file attivo
    def get_active_file(self):
        return self.file_manager.get_active_file()
    
    # Cambia il file attivo
    def change_active(self, new_active_file: str):
        return self.file_manager.change_active(new_active_file)

    def save(self, phrase: str):
        self.file_manager.save(phrase)

    def delete_file(self, file_to_delete:str):
        return self.file_manager.delete(file_to_delete)

    # Recupera i nomi dei file
    def get_files(self):
        return self.file_manager.get_files()

    # Crea un dizionario con tutte le info
    def user_to_table(self) -> dict:
        return { 
            'id': self.id, 
            'name': self.name,
            'files' : self.file_manager.get_files()
        }

    # Crea una stringa json
    def user_to_json(self) -> str:
        return json.dumps(self.user_to_table())