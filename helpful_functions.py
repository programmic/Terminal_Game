import colors as colors
from colorsys import hsv_to_rgb
from math import sqrt, acos, exp
from functools import wraps
import time
import os

clear = "\033c"

def time_it(func):
    """
    Decorator that measures the runtime of the function it decorates.

    Args:
        func: The function to be decorated.

    Returns:
        The wrapper function that measures and prints the execution time.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Call the original function
        end_time = time.time()  # Record the end time
        duration = end_time - start_time  # Calculate the duration
        print(f"Function '{func.__name__}' took {duration:.4f} seconds to complete.")
        return result  # Return the original function's result
    return wrapper

def readFile(pName: str, pNr: int, extension: str = ".txt") -> list[str]:
    """
    Reads a file ending with a number, usefull when multible similar files are in use, like different tasks or configs

    Args:
        pName (String): Path to the file location and file name
        pNr (int): Files number for iterating through similar files
        extension (String): Files file extension. Defaults to '.txt'
        removeEmpty (Boolean): Toggles wether empty lines are removed.Defaults to True

    Returns:
        Array: array of Strings, each String a line
    """
    dateiname = pName + str(pNr) + extension
    with open(dateiname, "r", encoding = "utf-8") as data:
        tmp = data.read().split("\n")
        ausgabe = []
        for i in tmp:
            if not i == "":
                ausgabe.append(i)
    return ausgabe


def lenformat( pInput: str | int, pDesiredLength: int, character: str = " ", place: str = "back" ) -> int:
    """
    Extends the length of a given string or integer to a specified length for prettier terminal output

    Args:
        pInput (string, int): The text that is to be formated
        pDesiredLength (int): Amount of characters the text should occupy
        character (str, optional): Characters used to fill blank space.\nDefaults to " ".
        place (str, optional): Defines wether characters should be placed in front or behind text.\n
            Accepts: "front", "back"\n
                Defaults to "back"

    Returns:
        String: String, formated to fit your needs
    """
    if place == "back":
        return str(str(pInput) + str(character * int(int(pDesiredLength) - len(str(pInput)))))
    elif place == "front":
        return str(character * int(int(pDesiredLength) - len(str(pInput)))) + str(str(pInput))
    
def progress(percentage: float | int, length: int, empty: str = "-", filled: str = "#", braces: str = "[]"):
    if braces == " " or braces == "": braces = "  "
    filled_length = int(length * percentage)

    return(  braces[ 0 ] + ( filled * filled_length ) + ( empty * ( length - filled_length -1 ) ) + braces[1])
    
def clearTerminal() -> None:
    """
    clears the Terminal
    """
    print("\033c", end="")  # Clears Python Console Output

def clearLastTerminalLine() -> None:
    print(f"{colors.CURSOR_UP}{colors.CURSOR_ERASE_LINE}",end="")

def get_terminal_width() -> int:
    """Gets the width of the terminal in characters."""
    return os.get_terminal_size().columns

def calculate_wrapped_lines(text: str, terminal_width: int) -> int:
    """
    Calculates how many lines a text will take up in the terminal considering wrapping.
    
    Args:
        text (str): The text to be printed.
        terminal_width (int): The width of the terminal.
    
    Returns:
        (int): The number of lines the text will take up.
    """
    wrapped_lines = wrap_text(text, terminal_width)
    return len(wrapped_lines)

def wrap_text(text: str, width: int) -> list[str]:
    """
    Wrap the text into a list of lines, ensuring that no line exceeds the terminal width.
    
    Args:
        text (str): The text to wrap.
        width (int): The maximum width of the terminal.
    
    Returns:
        list[str]: A list of wrapped lines.
    """
    words = text.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        # Add the word to the current line if it fits within the width
        if len(current_line) + len(word) + 1 <= width:
            current_line += (word + ' ')
        else:
            # If the word doesn't fit, move the current line to the list and start a new line
            lines.append(current_line.strip())
            current_line = word + ' '
    
    # Add the last line if there's remaining text
    if current_line:
        lines.append(current_line.strip())
    
    return lines

def print_wrapped_text(text: str) -> None:
    """
    Prints the text with manual wrapping to avoid issues with terminal automatic line wrapping.
    
    Args:
        text (str): The text to print.
    """
    terminal_width = get_terminal_width()
    wrapped_lines = wrap_text(text, terminal_width)
    
    for line in wrapped_lines:
        print(line)

def clear_lines(num_lines: int) -> None:
    """
    Clears the specified number of lines from the terminal output.
    
    Args:
        num_lines (int): The number of lines to clear.
    """
    for _ in range(num_lines):
        print("\033[F\033[K", end='')  # Move cursor up and clear the line


def makeMatrix(
        pX: int, 
        pY: int, 
        pZ:int =1
        ) -> list:
    """
    Easy way to quickly generate empty matrix
    Args:
        pX (int): matrix x dimension
        pY (int): matrix y dimension
        pY (int): matrix z dimension.\n
            Defaults to 1

    Returns:
        matrix (array): 2-Dimensional, empty data matrix
    """
    ret = []
    for i in range (pY):
        ret.append([])
        for j in range( pX ):
            ret[i].append([])
            if pZ > 1:
                for n in range(pZ):
                    ret[i][j].append([])  
    return ret

def transpose(matrix):
    """
    Transposes the given matrix (rows become columns and vice versa).

    Parameters:
    matrix (list of lists): The matrix to be transposed.

    Returns:
    list of lists: The transposed matrix.
    """
    return [list(row) for row in zip(*matrix)]

def HSVpercentToRGB(
        H: float, 
        saturation: float = 100, 
        value: float = 100
        ) -> tuple[ float, float, float ]:
    """
    Gibt den RGB-Wert basierend auf dem Prozentsatz durch den Hue-Wert zurück.
    Args:
        percentage (int): Ein Prozentsatz (0 bis 100), der angibt, wie weit man durch den Hue-Wert fortgeschritten ist.
    Returns:
        RBG (tupel): Ein Tupel (R, G, B) mit den RGB-Werten.
    """
    if not (0 <= H <= 100):
        raise ValueError("Percentage must be between 0 and 100")
    hue = (H / 100.0) * 360
    hue_normalized = hue / 360.0
    r, g, b = hsv_to_rgb(hue_normalized, saturation/100, value/100)
    
    return (float(r * 255), float(g * 255), float(b * 255))

def RGBtoKivyColorCode(color: tuple) -> tuple[ float, float, float ]:
    """
    | Converts a color from standart RGB color space to Kivy color space,
    | which is clamped between ```0-1``` instead of the normal ```0-25```

    Args:
        colorRGB  (tuple): Takes a ```0 - 255``` RBG Tupel ```(R, G, B)```
    Returns:
        colorKivy (tuple): returns same color value in Kivy color space
    """
    return( float(color[ 0 ] / 255 ), float( color[ 1 ] / 255 ), float(color[ 2 ] / 255 ) )

def normalizeVector(vector: tuple) -> tuple:
    """
    Normalizes a given *n*-dimensional vector\n
    .. math:: ∥V∥ = sqrt( v^(2/1) + v^(2/2) + ⋯ + v^(2/n) )

    Args:
        vector (tuple): *n*-dimensional vector

    Raises:
        ValueError: does not accept zero vector

    Returns:
        tuple: normalized vector
    """
    # Calculate the magnitude of the vector
    magnitude = sqrt(sum(v**2 for v in vector))
    
    # Avoid division by zero
    if magnitude == 0:
        raise ValueError("Cannot normalize a zero vector")
    
    # Divide each component by the magnitude
    return [v / magnitude for v in vector]

def vector_add(v1, v2):
    """
    Adds two vectors element-wise.

    Parameters:
    v1 (list): The first vector.
    v2 (list): The second vector.

    Returns:
    list: The resulting vector after addition.
    """
    return [a + b for a, b in zip(v1, v2)]

def vector_subtract(v1, v2):
    """
    Subtracts the second vector from the first vector element-wise.

    Parameters:
    v1 (list): The first vector.
    v2 (list): The second vector.

    Returns:
    list: The resulting vector after subtraction.
    """
    return [a - b for a, b in zip(v1, v2)]

def intersectsLineVec(
        p1 :  tuple [ float, float ],
        p2 :  tuple [ float, float ],
        vec : tuple [ float, float ],
        dir : tuple [ float, float ]
        ) -> bool:
    pass

def dot(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def dot2(vector1, vector2):
    """
    Calculate the dot product of two 2D vectors.
    
    Parameters:
    vector1: list or tuple of 2 elements (x1, y1)
    vector2: list or tuple of 2 elements (x2, y2)
    
    Returns:
    The dot product of the two vectors.
    """
    if len(vector1) != 2 or len(vector2) != 2:
        raise ValueError("Both vectors must have exactly 2 elements.")
    
    return vector1[0] * vector2[0] + vector1[1] * vector2[1]

def dot3(vector1, vector2):
    """
    Calculate the dot product of two 3D vectors.
    
    Parameters:
    vector1: list or tuple of 3 elements (x1, y1, z1)
    vector2: list or tuple of 3 elements (x2, y2, z2)
    
    Returns:
    The dot product of the two vectors.
    """
    if len(vector1) != 3 or len(vector2) != 3:
        raise ValueError("Both vectors must have exactly 3 elements.")
    
    return vector1[0] * vector2[0] + vector1[1] * vector2[1] + vector1[2] * vector2[2]

def scalar_vector_mult(scalar, vector):
    """
    Multiplies a scalar with each element of the vector.

    Parameters:
    scalar (float or int): The scalar value.
    vector (list or array): The vector with which the scalar is multiplied.

    Returns:
    list: A new vector resulting from the scalar-vector multiplication.
    """
    return [scalar * element for element in vector]

def mag3(vector):
    """
    Calculate the magnitude of a 3D vector.
    
    Parameters:
    vector: list or tuple of 3 elements (x, y, z)
    
    Returns:
    The magnitude of the vector.
    """
    return sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

def mag2(vector):
    """
    Calculate the magnitude of a 2D vector.
    
    Parameters:
    vector: list or tuple of 3 elements (x, y)
    
    Returns:
    The magnitude of the vector.
    """
    return sqrt(vector[0]**2 + vector[1]**2)

def vec2angleRad(vector1, vector2):
    """
    Calculate the angle between two 2D vectors in radians.
    
    Parameters:
    vector1: list or tuple of 2 elements (x1, y1)
    vector2: list or tuple of 2 elements (x2, y2)
    
    Returns:
    The angle between the two vectors in radians.
    """
    dot_prod = dot2(vector1, vector2)
    magnitude_v1 = mag2(vector1)
    magnitude_v2 = mag2(vector2)
    
    # Calculate cosine of the angle using the dot product formula
    cos_angle = dot_prod / (magnitude_v1 * magnitude_v2)
    
    # To avoid floating point inaccuracies, ensure the value is in the range [-1, 1]
    cos_angle = max(min(cos_angle, 1), -1)
    
    # Calculate the angle in radians
    angle_radians = acos(cos_angle)
    
    return angle_radians

def vec3angleRad(vector1, vector2):
    """
    Calculate the angle between two 3D vectors in radians.
    
    Parameters:
    vector1: list or tuple of 3 elements (x1, y1, z1)
    vector2: list or tuple of 3 elements (x2, y2, z2)
    
    Returns:
    The angle between the two vectors in degrees.
    """
    dot_prod = dot3(vector1, vector2)
    magnitude_v1 = mag3(vector1)
    magnitude_v2 = mag3(vector2)
    
    # Calculate cosine of the angle using the dot product formula
    cos_angle = dot_prod / (magnitude_v1 * magnitude_v2)
    
    # To avoid floating point inaccuracies, ensure the value is in the range [-1, 1]
    cos_angle = max(min(cos_angle, 1), -1)
    
    # Calculate the angle in radians
    angle_radians = acos(cos_angle)
    
    return angle_radians

def timeFormat(seconds: int | float) -> str:
    # Extract days, hours, minutes, seconds, and milliseconds
    days = int(seconds // 86400)
    seconds %= 86400
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)

    # Format the output as dd:hh:mm:ss:msms
    return f"{days:02}d {hours:02}h {minutes:02}m {seconds:02}s {milliseconds:03}ms"
