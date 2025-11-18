"""
Main application entry point for the YouTube downloader.
"""

from sys import argv

from cli import is_one_line_command, run_cli_interactive_mode, run_cli_flags_mode



if __name__ == "__main__":
    if is_one_line_command(argv):
        run_cli_flags_mode()
    else:
        run_cli_interactive_mode()
