import json
from typing import Dict, Generator, List
import pandas as pd

FILES = ['EDIT\data.json','EDIT\data1.json','EDIT\data2.json']
DESTINATION_JSON_FILE = 'EDIT.json'
DESTINATION_EXCEL_FILE = 'EDIT.xlsx'

def line_generator(ln: str, *args: str) -> Dict:
    '''filter out  Serial and Name fields from the json line
    
    ToDo:
    Change static fields in the dictr file to args fields 
    '''

    arguments = [
        ags if isinstance(ags, list) else ags for ags in args
    ]

    for line in ln['params']:
        for l in line['data']:
            dictionary: dict = {}
            dictionary['name'] = l['name']
            dictionary["serial"] = l['serial'] if 'serial' in l else 'None'
            yield dictionary

def return_generator_from_json_line(line: list, *args: tuple) -> Generator:
    '''The *args should only be the keys of the dict.'''
    
    arguments = [
        ags if isinstance(ags, list) else ags for ags in args
    ]

    for ln in line:
        for l in ln:
            if isinstance(l, dict):
                for arg in arguments:
                    yield l[arg]

def parse_json_file(file_list) -> List:
    '''Parse a json file and return a list with specific keys.'''

    lst: list[dict] = []
    for json_file in file_list:
        with open(json_file, "r") as out_file:
            line = json.load(out_file)
            lst.append(list(line_generator(line)))
    return lst

def open_file_to_write(filename: str, lst: List[dict]) -> None:
    with open(filename, "w") as file_out:
        file_out.write(json.dumps(lst, indent=4))

def write_excell_file(data) -> None:
    '''Is expected to wirte data in the excell file.'''
    df = pd.DataFrame(data=data)
    df.to_excel(DESTINATION_EXCEL_FILE)

def open_file_reader(filename: str, *args: str) -> None:
    '''Given an json file and dict key *args you can return excel file. Mode will
    be used to differ between line by line or column.
    
     dict like this:
        {'arg1': [1, 2], 'agr2': [3, 4]}

    '''

    arguments: list[str] = [value for value in args]
    data_dict: dict = {}

    with open(filename, "r") as file_out:

        load_json = json.load(file_out)
        for arg in arguments:
            new_list_single_args = list(return_generator_from_json_line(load_json, arg))
            data_dict[arg] = new_list_single_args

    write_excell_file(data_dict)

def main():

    final_list = parse_json_file(FILES)

    open_file_to_write(DESTINATION_JSON_FILE, final_list)
    open_file_reader(DESTINATION_JSON_FILE, 'name', 'serial')

if __name__ == '__main__':
    
    main()    
