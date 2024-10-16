from helpful_functions import *

def findSegment(text: str, operator: str, terminate: str = "~") -> str:
    """
    Takes the text and the operator as an input, 
    and returns all items between it and the next 
    termination character (defaults to ~)

    Args:
        text (str): Full text, required for search
        operator (str): Identifier for Segment
        terminate (str): Character terminating segment

    Returns:
        (str): Segment
    """
    startIndex = text.find(operator)  # Find the index of the operator
    if startIndex == -1:
        print(f"Unable to find section {operator}")
        return ""
    
    endIndex = text.find(terminate, startIndex)  # Find the termination character starting from startIndex
    if endIndex == -1:
        print(f"Unable to find termination character '{terminate}' after {operator}")
        return ""
    
    # Slice the text between the operator and termination point
    return text[startIndex + len(operator) + 1 : endIndex]

def consoleFormat(text: str | list[str]) -> str | list[str]:
    delete = str.maketrans({"\n": ""})
    if isinstance(text, str):
        return text.translate(delete)  # Remove \n from the string
    elif isinstance(text, list):
        newlist = [i.translate(delete) for i in text]
        return newlist
    else:
        raise TypeError(f"Input given was {type(text)}, not str / list[str]\n{text}")

clearTerminal()

entryPoint:str = ">class"

compSeg = consoleFormat(findSegment(open("Story\charcaterSetup.txt").read(), entryPoint))

print(colors.green + compSeg + colors.clear)

if "&?" in compSeg: #question detected
    seperator = compSeg.find("&?")
    options: list[str] = consoleFormat(compSeg[seperator+2:]).split("%")
    options = list(filter(None, options))
    for i in options:
        print (i)
    colors.printBlue(options)


#print(seg, operator)