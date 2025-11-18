from utils import Downloader, print_array
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
    URL = ask_input("Enter URL : ",color="RED", style="BOLD", end="")
    downloader = Downloader(URL)

    # ---- SHOW OPTIONS
    print_s("Options : ",color="RED")
    for key, value in OPTIONS.items():
        print(f"[{key}] : {value} ")

    print_s("Choice number : ",color="RED",style="BOLD",sep="",end="")
    choice = input("")

    streams = None
    while True:
        if(choice == "1"):
            streams = downloader.get_streams(only_video=True)
            break
        elif(choice == "2"):
            streams = downloader.get_streams(only_audio=True)
            break
        elif(choice == "3"):
            streams = downloader.get_streams(progressive=True)
            break
        else:
            print_s("Warning wrong choise "+choice+" !!!",color="RED")

    itag = None
    directory = None
    file = None

    print_array(streams)
    print_s("Stream itag (enter the itag of the stream you want to download): ",color="RED",style="BOLD",sep="",end="")
    itag = input()

    print_s("Where do you want to save it : ",color="RED",style="BOLD",sep="",end="")
    directory = os.path.expanduser(input())

    print_s("What do you want to name it : ",color="RED",style="BOLD",sep="",end="")
    file  = input()

    full_path = os.path.join(directory, file)

    res = None

    with LoadingAnimation("Downloading... ") as load:
        load.switch_to_spinner() 
        res = downloader.download_stream(itag=int(itag),output_path=directory,filename=file)
    if(res):
        print_s("finished Downloading succefuly : "+downloader.yt.title+" as "+file,color="GREEN")
        print_s("FULL PATH : "+full_path,color="GREEN")
    else:
        print_s("\nDOWNLOAD FAILED !!!\n",color="RED",style="BOLD")
    return None


