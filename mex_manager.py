from secret_stuff import private_folder
import json
from user_info import UserInfo
from telegram import Message

default_mex = "Messaggio di default"

class MexManager:
    def __init__(self, mex_json_path:str) -> None:
        self.file_path = mex_json_path
        self.mex = MexManager.load_mex(self.file_path)

    def load_mex(file_name:str) -> list[dict]:
        mex_dict = []

        file_path = private_folder + file_name

        mex_json = open(file_path, 'r').readlines()

        entire_file = ""
        for line in mex_json:
            entire_file = entire_file + (line.replace("\n", '').replace('  ', ''))

        if entire_file != "":
            all_mex = json.loads(entire_file)
            for mex in all_mex:
                mex_dict.append({'id': mex['id'], 'formatting': mex['formatting'], 'format_value': mex['format_value'], 'code': mex['code'], 'value': mex['value']})
        
        return mex_dict

    def return_mex(self, mex_code:str, current_user:UserInfo, message: Message) -> str:
        mex_found = None
        for m in self.mex:
            if m['code'] == mex_code:
                mex_found = m
                break

        if mex_found == None:
            return default_mex
        
        result = mex_found['value']
        
        # Formatta il messaggio
        fill_placeholder = []

        for key in mex_found['format_value']:
            if key == "name":
                fill_placeholder.append(current_user.name)
            elif key == "id":
                fill_placeholder.append(current_user.id)
            elif key == "active_file":
                active_file = current_user.get_active_file()

                if active_file == None:
                    fill_placeholder.append("Nessun file attivo")
                else:
                    fill_placeholder.append(active_file)
            elif key == "text":
                fill_placeholder.append(message.text)
            elif key == "text_file":
                fill_placeholder.append((message.text).replace(' ', '_').lower())
            else:
                fill_placeholder.append("ERROR: NO KEY FOUND")

        result = result.format(*fill_placeholder)

        return result