# STATO : LISTA COMANDI UTILIZZABILI
# start : start, file, save, delete, about, back
# file : save, delete, change_active, back
# new_file : file, back
# save : file, back
# change_active : file, back
# delete : file, back

# state_cmd.json

from utility import get_json_string

class StateRule:
    def __init__(self, state:str, available_cmd: list[str], to_state: list[str]) -> None:
        self.state = state
        self.available_cmd = available_cmd
        self.to_state = [to_state]
    
    def get_state(self) -> str:
        return self.state
    
    def is_valid_command(self, cmd:str) -> int:
        for i in range(0, len(self.available_cmd)):
            if cmd == self.available_cmd[i]:
                return i
            
        return -1
    
    def get_new_state(self, idx:int) -> str:
        if idx == -1:
            return ''
        
        return self.to_state[idx]

class UserStateMachine:
    def __init__(self, rules_file:str) -> None:        
        rules = get_json_string(rules_file)

        self.state_rules = list[StateRule]
        for rule in rules:
            self.state_rules.append(StateRule(rule['state'], rule['available'], rule['to_state']))

        self.current_state = self.get_state_rule('start')

    def get_state_rule(self, search:str) -> StateRule:
        rule_found = None
        for rule in self.state_rules:
            if rule.get_state() == search:
                rule_found = rule
                break
        
        return rule_found
    
    def get_state(self) -> str:
        return self.current_state.get_state()

    def is_state(self, state) -> bool:
        return self.current_state.get_state() == state
    
    def change_state(self, cmd) -> bool:
        idx = self.current_state.is_valid_command(cmd)

        if idx == -1:
            return False
        
        new_state = self.current_state.get_new_state(idx)

        if new_state == '':
            return False
        
        self.current_state = self.get_state_rule(new_state)

        return True