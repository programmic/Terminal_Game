from helpful_functions import *
import os.path
import json

def saveToJSON(input: dict, file: os.PathLike | str) -> None:
    """
    Save a dictionary to a JSON file.

    Parameters:
    input (dict): The dictionary to save.
    file (os.pathLike |str): The file path where the JSON data will be stored.
    """
    with open(file, 'w') as json_file:
        json.dump(input, json_file, indent=4)

def loadJSONdictFile(input: os.PathLike | str) -> dict | dict[dict] | list[dict]:
    """
    Load items from a JSON file.

    Parameters:
    input (os.PathLike | str): The path to the JSON file.

    Returns:
    dict | dict[dict] | list[dict]: The loaded data, with varying types based on JSON structure.
    """
    with open(input, 'r') as json_file:
        data = json.load(json_file)
    return data

def __loadItemJsonBase(file:os.PathLike | str | list[dict] | dict[dict]) -> dict:
    if type(file) == os.PathLike or str:
        items = loadJSONdictFile(file)
    else: items = file
    return items

def loadItemJson(input: str, file:os.PathLike | str | list[dict] | dict[dict], findBy: str = "ID") -> dict:
    items:dict = __loadItemJsonBase(file=file)
    legalIdentifiers: list = []
    if type(items) == list:
        for i in items:
            for n in i.keys():
                if not n in legalIdentifiers:
                    legalIdentifiers.append(n)
    else: legalIdentifiers = [ items.keys() ]
    if not findBy in legalIdentifiers: 
        raise ValueError(f"{colors.red}Items provided by \"loadItemJson\" has no identifier \"{colors.ITALIC}{findBy}{colors.clear}{colors.red}\"\nSupported Identifiers are: {legalIdentifiers}{colors.clear}")
    for i in items:
        if i[findBy] == input: return i
    return None 

def loadItemsJson(input: str, file:os.PathLike | str | list[dict] | dict[dict], findBy: str = "ID") -> list[dict]:
    items:dict = __loadItemJsonBase(file=file)
    legalIdentifiers: list = []
    if type(items) == list:
        for i in items:
            for n in i.keys():
                if not n in legalIdentifiers:
                    legalIdentifiers.append(n)
    else: legalIdentifiers = [ items.keys() ]
    if not findBy in legalIdentifiers: 
        raise ValueError(f"{colors.red}Items provided by \"loadItemJson\" has no identifier \"{colors.ITALIC}{findBy}{colors.clear}{colors.red}\"\nSupported Identifiers are: {legalIdentifiers}{colors.clear}")
    matches: list = []
    for i in items:
        if input in i[findBy]: 
            matches.append(i)

    if len(matches) >=1: return matches 
    else: return None 

if __name__ == "__main__":
    file = os.path.abspath('C:/Users/Simon/Documents/Python/Terminal_Game/Data/Items/Weapons/Melee/Melee.json')
    print( [i for i in loadItemsJson("Leach", file, "Eigenschaften")])