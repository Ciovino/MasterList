import json

def get_json_string(json_file_name:str) -> list[dict]:
    all_lines = open(json_file_name, 'r').readlines()

    entire_file = ""
    for line in all_lines:
        entire_file = entire_file + (line.replace("\n", '').replace('  ', ''))

    return_list = []

    if entire_file != "":
        return_list = json.loads(entire_file)

    return return_list