from secret_stuff import private_folder
import json

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
                mex_dict.append({'id': mex['id'], 'code': mex['code'], 'value': mex['value']})
        
        return mex_dict

    def return_mex(self, mex_code:str) -> str:
        mex_found = None
        for m in self.mex:
            if m['code'] == mex_code:
                mex_found = m
                break

        if mex_found != None:
            return mex_found['value']
        else:
            return default_mex