import json
from helpful_functions import *

def readSegment(text: str):
    frag: str = ""
    cmd: str = ""
    stop: bool = False
    for i in text:
        if not i == "$" and not stop:
            frag += i
        elif i == "$" and stop:
            break
        else:
            stop = True
            if i != "$": cmd += i 
    return (frag, cmd)

def findSegment(text: str, operator: str):
    index = text.find(operator)  # Find the index of the first occurrence of the letter
    print(f"Index: {index}\nLetters from index: {text[index : index+15]}")
    if index != -1:  # If the letter is found in the string
        return text[index + 1 + len(operator):]  # Return everything after the letter
    return ""  # Return an empty string if the letter is not found

def segmentize(text, curSeg):
    frag, nextSeg = readSegment(findSegment(text, curSeg))
    return frag, nextSeg

##############################################################
#############           MAIN                   ###############
##############################################################

clearTerminal()

with open("Story\charcaterSetup.txt", "r") as characterSetup:
    text: str = characterSetup.read()

    startSeg = ">operatorlengthtest"

    segment, operator = segmentize(text, startSeg)
    print(segment, " "*15, operator)
    while  operator != "none":
        segment, operator = segmentize(text, ">" + operator)
        print(segment, " "*15, operator)
        input("Tab Enter to continue")

    characterSetup.close()