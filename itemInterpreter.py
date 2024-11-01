from helpful_functions import *

def segmentize( fileToRead: str ) -> list[ str ]:
    with open(fileToRead, "r", encoding = "utf-8") as data: file: str = data.read() ; data.close()
    return file.strip().split( "$" )

def toAttributeList( dataset: str, returnAdvancedData:bool = False) -> dict:
    attributes = dataset.strip("\n\n").split("\n")
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

def getDataset(datasets: list[str], identifier: str) -> str:
    for dataset in datasets:
        if (('#' in identifier and identifier in dataset) or
            (not '#' in identifier and f"name={identifier.lower()}" in dataset.lower())):
            return dataset
    raise ValueError ("Dataset not found")  # Return a message if no match is found
        
def printInfoSheet(filename: str, datasetName: str) -> None:
    datasets = segmentize(filename)
    dataset = getDataset( datasets, datasetName)
    attributes, keys, vals = toAttributeList(dataset, returnAdvancedData=True)
    for key in keys:
        print(str(lenformat(key, 13, place="front")) + "  -  " + str(attributes[key]))

if __name__ == "__main__":
    printInfoSheet("C:/Users/Simon/Documents/Python/Terminal_Game/Data/Items/Weapons/Melee/Melee.txt","seelenspalter")