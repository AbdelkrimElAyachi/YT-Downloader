"""
This modules provices utility for styling cli functions like print
"""
from typing import Optional
import os

# ANSI color codes
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGNETA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"  # Reset to default color

# Bold, underline, etc.
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

# pylint: disable=keyword-arg-before-vararg
def print_s(message:str, color:Optional[str]="WHITE", style:Optional[str]=None, *args, **kwargs):
    """
    A modified version of print() that works with differents style

    Arguments:
        color(str,optional): Takes the color you want the text to be displayed in 
        list of possible colors : BLACK RED GREEN YELLOW BLUE MAGNETA CYAN WHITE
        By default takes WHITE
        style(str,optional): Takes the style you want to apply to the text 
        list of pssible styles : UNDERLINE, BOLD
        by default takes None
    """
    colors_array = ["BLACK","RED","GREEN","YELLOW","BLUE","MAGNETA","CYAN","WHITE"]
    styles_array = ["BOLD","UNDERLINE"]

    colors_list = {
        "BLACK" : BLACK,
        "RED" : RED,
        "GREEN" : GREEN,
        "YELLOW" : YELLOW,
        "BLUE" : BLUE,
        "MAGNETA" : MAGNETA,
        "CYAN" : CYAN,
        "WHITE" : WHITE,
        "RESET" : RESET
    }

    styles_list = {
        "BOLD": BOLD,
        "UNDERLINE": UNDERLINE
    }

    if color:
        if color.upper() in colors_array:
            print(colors_list[color.upper()], end="", sep="")
        else:
            raise ValueError("Unsupported colors : ", color)

    if style:
        if style.upper() in styles_array:
            print(styles_list[style.upper()], end="", sep="")
        else:
            raise ValueError("Unsupported style : ", style)

    print(message+colors_list["RESET"], *args, **kwargs)


def starter_message(message):
    "Display the start message of the application in cli modes both interactive and oneline mode"
    try:
        console_width = os.get_terminal_size().columns - 1
    except OSError:
        console_width = 50
    half_csl = (console_width-len(message))//2
    msg = half_csl*"-"+message+half_csl*"-"
    print_s(message=msg,color="RED")
