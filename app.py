"""
Main application entry point for the YouTube downloader.
Supports three modes: interactive CLI, one-line flags CLI, and GUI.
"""

from sys import argv

from cli import is_one_line_command, run_cli_interactive_mode, run_cli_flags_mode, starter_message


if __name__ == "__main__":
    starter_message("YT Stream Downloader")

    if "--gui" in argv:
        from gui import start_gui
        start_gui()
    elif is_one_line_command(argv):
        run_cli_flags_mode()
    else:
        run_cli_interactive_mode()
