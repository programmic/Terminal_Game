from helpful_functions import *

def cleanInput(prompt="Enter value: ") -> int:
    out = input(prompt)  # Show a prompt message for the user
    clearLastTerminalLine()  # Optional: remove the input line from the terminal display
    return out

def consoleFormat(text: str | list[str]) -> str | list[str]:
    delete = str.maketrans({"\n": ""})
    if isinstance(text, str):
        return text.translate(delete)  # Remove \n from the string
    elif isinstance(text, list):
        newList = [i.translate(delete) for i in text]
        return newList
    else:
        raise TypeError(f"Input given was {type(text)}, not str / list[str]\n{text}")

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

def extract_options_from_segment(segment: str) -> dict:
    """
    Extracts the options from a segment more reliably.

    Args:
        segment (str): The segment containing the options.

    Returns:
        (dict): A dictionary where the key is the displayed option and the value is the segment identifier.
    """
    options_start = segment.find("&/")
    if options_start == -1:
        return {}

    # Find all the options that start with `%`
    options_part = segment[options_start + 2:]  # Ignore the &/ marker
    options = options_part.split("%")
    
    questions = {}
    for option in options:
        if "|" in option:  # For cases where we use "|" like class selection
            option_text, next_segment = option.split("|")
            option_text = option_text.strip()
            next_segment = next_segment.strip()
            if option_text and next_segment:
                questions[option_text] = next_segment

    return questions

def load_save_file(filename: str) -> str:
    """
    Loads the content of the save file.

    Args:
        filename (str): The path to the save file.
    
    Returns:
        (str): The content of the file.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def get_segment(content: str, entry_point: str) -> str:
    """
    Gets the relevant segment from the save file content.

    Args:
        content (str): The full text from the save file.
        entry_point (str): The point at which to start the segment.

    Returns:
        (str): The segment.
    """
    return findSegment(content, entry_point)

def parse_options(segment: str) -> dict:
    """
    Parses the options in the segment and returns a dictionary of choices.

    Args:
        segment (str): The input string containing options.

    Returns:
        (dict): Dictionary of options, where key is the displayed option and value is the next segment identifier.
    """
    separator = segment.find("&/")
    if separator == -1:
        return {}

    options = consoleFormat(segment[separator + 2:]).split("%")
    options = list(filter(None, options))

    questions = {}
    for i in options:
        key_value = i.split("|")
        if len(key_value) == 2:
            questions[key_value[0]] = key_value[1]

    return questions

def handleTextVariables(text: str) -> None: # [?gender male|Sein female|Ihr nonbinary|They]
    while "&*" in text:
        startIdx = text.find("&*") + 2
        endIdx = text.find("*", startIdx)
        if endIdx == -1:
            raise SyntaxError("Error: No closing '*' found.")
        
        operator = text[startIdx:endIdx]
        
        if "=" in operator:
            var, val = operator.split("=")
            attributes[var] = val
        elif "+" in operator:
            var,val = operator.split("+")
            attributes[var] = int (attributes[var]) + int(val)
        elif "-" in operator:
            var,val = operator.split("-")
            if int(attributes[var]) - int(val) < 0:
                raise ValueError(f"Error: Characters stats may not be negative\n{attributes[var]} - {val} = {int(attributes[var]) - int(val)}")
            attributes[var] = int(attributes[var]) - int(val)
        else:
            var = operator.strip()
            val = cleanInput(f"Enter value for {var}: ")
            attributes[var] = val

        text = text[endIdx + 1:]

def display_question_and_get_answer(questions: dict) -> str:
    """
    Displays the options to the user and gets the player's choice.
    Clears only the options after a choice is made.
    
    Args:
        questions (dict): Dictionary of options.

    Returns:
        (str): The selected choice (corresponding to the next segment identifier).
    """
    # Get the terminal width to account for line wrapping
    terminal_width = get_terminal_width()
    
    # Display options to the user and keep track of how many lines were printed
    lines_printed = 0
    print()
    for idx, option in enumerate(questions.keys(), 1):
        option_text = f"  {colors.blue}{' '*3}[{lenformat(idx, len(str(len(questions.keys()))), place='front')}]{colors.clear} {option}\n"
        printAnimated(option_text, sps=25)
        # Calculate how many lines this option will take up considering wrapping
        lines_printed += calculate_wrapped_lines(option_text, terminal_width)

    attempts = 0
    max_attempts = 7

    while attempts < max_attempts:
        printAnimated("Choose your option ", sps= 25, doLineBreak=False)
        playerSel = cleanInput("")
        try: # Try Index Keying
            playerSel = int(playerSel) - 1  # Convert to zero-indexed
            if 0 <= playerSel < len(questions):
                selected_key = list(questions.keys())[playerSel]

                clear_lines(lines_printed)  # Also clearing the prompt line
                return questions[selected_key]
        except ValueError:
            # Try to match user input directly to a key
            if playerSel in questions:
                return questions[playerSel]
            else:
                for key in questions.keys():
                    if playerSel.lower() == key.lower():
                        # Clear the options (but not the text above them)
                        clear_lines(lines_printed)  # Also clearing the prompt line
                        return questions[key]
        attempts += 1
        if not playerSel == "\x0D": print(f"Invalid input. {max_attempts - attempts} attempts left.",end="\r")
        else: print(f"{colors.darkmagenta}")

    print("Maximum attempts reached.")
    return ""

def resolveFileLink(segment: str) -> str:
    """
    Checks if the segment contains a file link operator (&#) and returns the file name if present.

    Args:
        segment (str): The text of the current segment.

    Returns:
        (str): The name of the file to load if &# is present, else an empty string.
    """
    
    file_start = segment.find("&#") + len("&#")
    file_end = segment.find(" ", file_start)
    if file_end == -1:
        file_end = len(segment)  # In case the filename is the last thing in the segment
    return segment[file_start:file_end].strip()

def resolveAliases(segment: str, player_attributes: dict) -> str:
    """
    Resolves any placeholders in the segment based on player attributes.
    Placeholders are in the format [?variable option1:replacement1 option2:replacement2 ...]
    Accepts the [MC] placeholder for the player's name.

    Args:
        segment (str): The input segment containing placeholders.
        player_attributes (dict): The player's attributes.

    Returns:
        str: The resolved text with placeholders replaced by the appropriate values.
    """
    placeholder_start = segment.find("[?")
    while placeholder_start != -1:
        placeholder_end = segment.find("]", placeholder_start)
        if placeholder_end == -1:
            raise ValueError(f"{colors.red}Value Replacement Error:\nNo closing bracket found{colors.clear}")
            # No closing bracket found
# Extract the placeholder text (ignoring the "[?" part)
        placeholder_text = segment[placeholder_start + 2:placeholder_end]
        options = placeholder_text.split()

        # Text before the placeholder
        resolved_text = segment[:placeholder_start]
        varName = options[0]
        if varName in player_attributes:
            varVal = str(player_attributes[varName]).lower()
            replaced = False
            # Loop over all options (each in the format "option:replacement")
            for option in options[1:]:
                # Use maxsplit=1 in case the replacement text contains colons
                parts = option.split(":", 1)
                if len(parts) != 2:
                    colors.printRed(f"Value Replacement Error: Option '{option}' is not in the format 'option:replacement'.")
                    continue
                option_key, replacement = parts[0].lower(), parts[1]
                if option_key == varVal:
                    resolved_text += replacement
                    replaced = True
                    break  # Exit after the first match
            if not replaced:
                # If no matching option is found, you can choose to insert a default value
                # or simply append nothing.
                colors.printRed(f"Value Replacement Error: No matching entry for '{varName}' with value '{player_attributes[varName]}' found.")
        else:
            colors.printRed(f"Value Replacement Error: Variable '{varName}' not found in player attributes.")
        
        # Append the remaining text
        resolved_text += segment[placeholder_end + 1:]
        segment = resolved_text  # Update the segment for further placeholders
        placeholder_start = segment.find("[?")
    
    # Finally, replace [MC] with the player's name if present
    if "name" in player_attributes:
        segment = segment.replace("[MC]", str(player_attributes["name"]))
    else:
        colors.printRed("Value Replacement Error: 'name' not found in player attributes.")
    return segment

def printText(t: str, ttw: float = 1.0, sps: int = 20, mode="sps") -> None:
    """
    Writes the given text, niceley formated.

    Args:
        t (str): text
        ttw (float, optional): Total Time Waited. Defaults to 1.0.
        sps (int, optional): Symbols per second. Defaults to 8.
        mode (str, optional): Determines. Defaults to "sps". Accepst: "sps" (symbols per second), "ttw" (total time waited)
    """
    text = f"\n{resolveAliases(t.split('&')[0], attributes)}"
    printAnimated(text, ttw, sps, mode)
    
def main_game_loop(save_content: str) -> None:
    """
    Game loop with text segments and reliable parsing for options.
    
    Args:
        save_content (str): The full content of the save file.
    """
    global attributes
    attributes = { 
        "gender":"Undefined",
        "name":"Undefined",
        "class":"None",
        "money":0,
        "health":150,
        "mana":75,
        "damage_unarmed":5,
        "intelligence":10,
        "strength":10
        }
    global entity
    entity = []
    current_segment = ">start" # Start point of the game

    while current_segment:
        segment_text = get_segment(save_content, current_segment)

        if not segment_text:
            print(f"Unable to find segment for {current_segment}. Exiting.")
            break

        # Print the segment text directly
        printText(segment_text)

        if "&/" in segment_text:  # Check if the segment contains options
            if "&*" in segment_text: colors.printRed("Error: Text input within MCQ")
            questions = extract_options_from_segment(segment_text)
            if not questions:
                print("No valid options found. Exiting.")
                break

            next_segment = display_question_and_get_answer(questions)
            if not next_segment:
                print("No valid next segment found. Exiting.")
                break

            current_segment = f">{next_segment}"
        else:
            if "&*" in segment_text:
                handleTextVariables(segment_text)
            # No options, chain to next segment without clearing
            next_segment_marker = segment_text.split("&")[-1].strip()
            current_segment = f">{next_segment_marker}"

        if "&#" in segment_text:
            linked_file = resolveFileLink(segment_text)
            new_file_content = load_save_file( f"Data/Story/{linked_file}.txt")
            if new_file_content:
                save_content = new_file_content  # Replace content with the new file's content
                current_segment = ">start"  # Start the game from the new file's first segment
                continue  # Restart the loop with the new content

if __name__ == "__main__":
    # Load the save file
    save_file_content = load_save_file("Data/Story/characterSetup.txt")
    #save_file_content = load_save_file("Story/prolog.txt")
    
    # Start the game loop
    clearTerminal()
    main_game_loop(save_file_content)