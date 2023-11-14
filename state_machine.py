from utility import get_json_string
from secret_stuff import private_folder

class State:
    def __init__(self, id:int, name:str, type:list[str], link:list[int]) -> None:
        self.id = id
        self.name = name
        self.type = type
        self.link = link

        #print(f'{self.id} {self.name} {self.link}')
    
    def get_id(self) -> int:
        return self.id
    
    def get_name(self) -> str:
        return self.name
    
    def is_valid_type(self, type:str) -> bool:
        return type in self.type
    
    def allowed_change(self, new_state:int) -> bool:
        return new_state in self.link

class StateMachine:
    def __init__(self, state_file:str) -> None:
        all_state = get_json_string(private_folder + state_file)

        self.states = []
        for state in all_state:
            self.states.append(State(state['id'], state['name'], state['type'], state['link']))

        self.current_state = self.states[0]
        self.previous_state = self.states[0]

    def get_current_state(self) -> str:
        return self.current_state.get_name()
    
    def get_previous_state(self) -> str:
        return self.previous_state.get_name()

    def convert_name_to_id(self, name:str) -> int:
        state_found = State
        for state in self.states:
            if state.get_name() == name:
                state_found = state
                break
        
        if state_found is None:
            return -1
        
        return state_found.get_id()

    def convert_id_to_name(self, id:int) -> str:
        if id >= len(self.states):
            return ''
        
        return self.states[id].get_name()
    
    def valide_state_from_id(self, id:int) -> bool:
        return id < len(self.states) and id >= 0

    def valid_state(self, name:str) -> bool:
        id = self.convert_name_to_id(name)
        #print(id)

        return self.valide_state_from_id(id)
    
    def valid_command(self) -> bool:
        return self.current_state.is_valid_type('cmd')
    
    def valid_mex(self) -> bool:
        return self.current_state.is_valid_type('mex')

    def valid_query(self) -> bool:
        return self.current_state.is_valid_type('query')
    
    def get_state(self, name:str) -> State:
        if not self.valid_state(name):
            return None
        
        id = self.convert_name_to_id(name)

        return self.states[id]

    def change(self, cmd:str) -> bool:
        new_state = self.get_state(cmd)

        if new_state == None:
            return False
        
        if not self.current_state.allowed_change(new_state.get_id()):
            return False

        self.previous_state = self.current_state
        self.current_state = new_state

        return True