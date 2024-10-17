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

def cleanInput(text: str = "Pick your Choice: ") -> int:
    out = input(text)
    clearLastTerminalLine()
    return out

def question(segment: str) -> None:
    """
    Parse the segment to extract options and present them to the user for selection.

    Args:
        segment (str): The input string containing options.
    """
    seperator = segment.find("&?")
    if seperator == -1:
        print("No options found.")
        return

    options: list[str] = consoleFormat(segment[seperator + 2:]).split("%")
    options = list(filter(None, options))

    questions: dict[str, str] = {}
    for i in options:
        print(i)
        key_value = i.split("|")
        if len(key_value) == 2:
            questions[key_value[0]] = key_value[1]

    colors.printBlue(options)
    colors.printMagenta(questions)

    max_attempts = 7
    attempts = 0

    while attempts < max_attempts:
        if attempts == 0:
            playerSel: str = cleanInput()
        else:
            playerSel:str = cleanInput("Invalid. Please retry: ")

        try:
            playerSel = int(playerSel)
            if playerSel < 1 or playerSel > len(questions):
                attempts += 1
                continue  # Skip to the next iteration of the loop
            print(f"{playerSel}: {questions[list(questions.keys())[playerSel - 1]]}")
            return (f">{questions[list(questions.keys())[playerSel - 1]]}") # Exit the function if the selection is valid
        except ValueError:
            if playerSel in questions:
                return ( f">{questions[playerSel]}" )
            else:
                for key in questions.keys():
                    if playerSel.lower() == key.lower():
                        return ( f">{questions[key]}" )
                attempts += 1

    print("Maximum attempts reached. Please read manual or learn typing.")


clearTerminal()

entryPoint:str = ">class"

compSeg = consoleFormat(findSegment(open("Story\charcaterSetup.txt").read(), entryPoint))

print(colors.green + compSeg + colors.clear)

if "&?" in compSeg: #question detected
    print(question(compSeg))


#print(seg, operator)