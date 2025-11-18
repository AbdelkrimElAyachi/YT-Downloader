"""
This module provides cli functions to handle different cli logic
"""

def is_one_line_command(argv):
    """
    function checks if there is more than one argument 
    (if it is true then the user using oe line command)
    """
    return len(argv)>1

# function responsible for reading command line argument
# EXAMPLE
# INPUT : py app.py --url="http://www.youtube.com/dudk2" --output_path="./videos" --format="video"
# OUTPUT : {'url': 'http://www.youtube.com/dudk2', 'output_path': './videos', 'format': 'video'}

def read_arguments(argv):
    """
    function that return list contains cli flags structured and easy to read
    """
    structured_command_line_arguments = {}
    for argument in argv:
        if argument.startswith('--'):
            structured_command_line_arguments[argument.split('=')[0][2::]] = argument.split('=')[-1]

    return structured_command_line_arguments
