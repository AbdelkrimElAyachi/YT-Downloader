import os
from sys import argv
from utils import Downloader, print_array
from cli import LoadingAnimation, printS, is_one_line_command


def starter_message():
    message = "WELCOME to YT DOWNLOADER"
    try:
        console_width = os.get_terminal_size().columns - 1
    except:
        console_width = 50
    half_csl = (console_width-len(message))//2
    printS(half_csl*"-"+message+half_csl*"-",color="RED")


def handle_cli_interactive_mode():
    starter_message()

    printS("enter url : ",color="RED",style="BOLD",sep="",end="")
    URL = input("")

    downloader = Downloader(URL)

    printS("Options : ",color="RED")
    print("[1] Videos only")
    print("[2] Audios only")
    print("[3] Both")

    printS("Choice number : ",color="RED",style="BOLD",sep="",end="")
    choice = input("")

    streams = None
    while True:
        if(choice == "1"):
            streams = downloader.get_videos_only()
            break
        elif(choice == "2"):
            streams = downloader.get_audios_only()
            break
        elif(choice == "3"):
            streams = downloader.get_videos()
            break
        else:
            printS("Warning wrong choise "+choice+" !!!",color="RED")

    itag = None
    directory = None
    file = None

    print_array(streams)
    printS("Stream itag (enter the itag of the stream you want to download): ",color="RED",style="BOLD",sep="",end="")
    itag = input()

    printS("Where do you want to save it : ",color="RED",style="BOLD",sep="",end="")
    full_path = os.path.expanduser(input())

    directory = os.path.dirname(full_path)
    file = os.path.basename(full_path)

    res = None

    with LoadingAnimation("Downloading... ") as load:
        load.switch_to_spinner() 
        res = downloader.download_stream(itag=int(itag),output_path=directory,filename=file)
    if(res):
        printS("finished Downloading succefuly : "+downloader.yt.title+" as "+file,color="GREEN")
        printS("FULL PATH : "+full_path,color="GREEN")
    else:
        printS("\nDOWNLOAD FAILED !!!\n",color="RED",style="BOLD")
    return None


def handle_cli_flags_mode():
    print("not implementd yet")
    return None



if __name__ == "__main__":
    if(is_one_line_command(argv)):
        handle_cli_flags_mode()
    else:
        handle_cli_interactive_mode()
