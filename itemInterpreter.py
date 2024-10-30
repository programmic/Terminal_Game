from helpful_functions import *

def segmentize( fileToRead: str ) -> list[ str ]:
    with open(fileToRead, "r", encoding = "utf-8") as data: file: str = data.read() ; data.close()
    return file.strip().split( "$" )

def toAttributeList( item: str, returnAdvancedData:bool = False) -> dict:
    attributes = item.strip("\n\n").split("\n")
    attributes = [ i.split( "=" ) for i in attributes ]
    for i in attributes:
        if i == ['']: 
            attributes.remove(i)
    attrDict: dict = {}
    if returnAdvancedData:
        keys, vals = [], []
    for n, a in attributes:
        key, val = n, a
        # Convert types if possible
        if val.isdigit():
            val = int(val)
        elif val.replace('.', '', 1).isdigit():
            val = float(val)
        elif val.lower() in ["true", "false"]:
            val = val.lower() == "true"
        attrDict[key] = val
        if returnAdvancedData: 
            keys.append(key)
            vals.append(val)

    if returnAdvancedData:
        return attrDict, keys, vals
    else:
        return attrDict

def searchItem(items: list[str], identifier: str) -> str:
    for item in items:
        if (('#' in identifier and identifier in item) or
            (not '#' in identifier and f"name={identifier.lower()}" in item.lower())):
            return item
    raise ValueError ("Item not found")  # Return a message if no match is found
        
def printInfoSheet(filename: str, itemName: str) -> None:
    items = segmentize(filename)
    item = searchItem( items, itemName)
    attributes, keys, vals = toAttributeList(item, returnAdvancedData=True)
    for key in keys:
        print(str(lenformat(key, 13, place="front")) + "  -  " + str(attributes[key]))

if __name__ == "__main__":
    printInfoSheet("C:/Users/Simon/Documents/Python/Terminal_Game/Items/Weapons/Melee/Axes.txt","seelenspalter")