from .cli_animations import LoadingAnimation
from .cli_styles import print_s, starter_message
from .cli_functions import is_one_line_command, read_arguments
from .cli_interactive import run_cli_interactive_mode
from .cli_flags import run_cli_flags_mode


APP_NAME = "cli utils package"
VERSION = "1.0.0"

__all__ = [
    "LoadingAnimation",
    "printS","is_one_line_command",
    "read_arguments", 
    "run_cli_interactive_mode", 
    "run_cli_flags_mode",
    "APP_NAME",
    "VERSION"
]
