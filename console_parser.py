_CONSOLE_OPERATOR: str = "%%%"

commands: dict = {
    "help": "for i in commands.keys(): print(i+':      '+ commands[i])",
    "undefined": "print('Command not found!')",
}


def readConsoleLine(input: str) -> str:
    input = input[len(_CONSOLE_OPERATOR):] # Console Operator entfernen

    commandList = input.split(" ")
    for i in range(len(commandList)):
        if commandList[i] in commands:
            exec(commands[commandList[i]])
            return

if __name__ == "__main__":
    readConsoleLine("%%%help")