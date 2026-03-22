import os

from utils import Downloader
from cli import LoadingAnimation, print_s

OPTIONS = {
    1: "Videos only",
    2: "Audios only",
    3: "Both"
}

def ask_input(question, **kwargs):
    print_s(question, **kwargs)
    return input("")

def run_cli_interactive_mode():
    # ----- URL
    url = ask_input("Enter URL : ", color="RED", style="BOLD", end="")

    try:
        downloader = Downloader(url)
    except ValueError as e:
        print_s(f"Error: {e}", color="RED", style="BOLD")
        return None

    # ---- SHOW OPTIONS
    print_s("Options : ", color="RED")
    for key, value in OPTIONS.items():
        print(f"[{key}] : {value} ")

    streams = None
    while streams is None:
        print_s("Choice number : ", color="RED", style="BOLD", sep="", end="")
        choice = input("")

        if choice == "1":
            streams = downloader.get_streams(only_video=True)
        elif choice == "2":
            streams = downloader.get_streams(only_audio=True)
        elif choice == "3":
            streams = downloader.get_streams(progressive=True)
        else:
            print_s(f"Warning: wrong choice '{choice}' !!!", color="RED")

    for stream in streams:
        print(stream)

    print_s("Stream itag (enter the itag of the stream you want to download): ", color="RED", style="BOLD", sep="", end="")
    itag_input = input()

    try:
        itag = int(itag_input)
    except ValueError:
        print_s(f"Error: '{itag_input}' is not a valid itag number.", color="RED", style="BOLD")
        return None

    print_s("Where do you want to save it : ", color="RED", style="BOLD", sep="", end="")
    directory = os.path.expanduser(input())

    print_s("What do you want to name it : ", color="RED", style="BOLD", sep="", end="")
    filename = input()

    full_path = os.path.join(directory, filename)

    res = None
    try:
        with LoadingAnimation("Downloading... ") as load:
            load.switch_to_spinner()
            res = downloader.download_stream(itag=itag, output_path=directory, filename=filename)
    except RuntimeError as e:
        print_s(f"\nDOWNLOAD FAILED: {e}\n", color="RED", style="BOLD")
        return None

    if res:
        print_s(f"Finished downloading successfully: {downloader.yt.title} as {filename}", color="GREEN")
        print_s(f"FULL PATH: {full_path}", color="GREEN")
    else:
        print_s("\nDOWNLOAD FAILED !!!\n", color="RED", style="BOLD")

    return None


