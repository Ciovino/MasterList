# Gestisce la scrittura/lettura/salvataggio dei file privati dell'utente

class UserFileManager:
    def _init_(self, id:int, user_file:list[str]):
        self.user_id = id
        self.active_file = None
        self.files = user_file
    
    def add_file(self, new_file_name:str):
        pass

    def save(self, info:str):
        pass
