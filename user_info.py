import json
from user_file_manager import UserFileManager
from state_machine import StateMachine

# Racchiude tutte le informazioni di un utente

class UserInfo:
    def __init__(self, id:int, name:str, files:list) -> None:
        self.id = id
        self.name = name
        self.state = StateMachine('bot\\state.json')

        self.file_manager = UserFileManager(id, files)

    def is_valid_command(self, cmd: str) -> bool:
        return self.state.valid_state(cmd)

    def is_mex_state(self) -> bool:
        return self.state.valid_mex()
    
    def is_query_state(self) -> bool:
        return self.state.valid_query()

    def change_state(self, cmd:str) -> bool:
        if not self.is_valid_command(cmd):
            return False

        return self.state.change(cmd)
    
    def return_to_home_state(self) -> None:
        self.state.return_to_home_state()
    
    def get_current_state(self) -> str:
        return self.state.get_current_state()
    
    def get_previous_state(self) -> str:
        return self.state.get_previous_state()

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

    def save_at_index(self, phrase:str, idx:int) -> bool:
        return self.file_manager.save_at_index(phrase, idx)

    def show(self) -> list[str]:
        return self.file_manager.show()

    def delete_line(self, line_to_delete: int) -> int:
        return self.file_manager.delete_line(line_to_delete - 1)

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