from downloader import Downloader
import os
import logging
from cli import LoadingAnimation, printS
from pprint import pprint

# variables we are going to use
URL = None

def print_array(array):
    for ele in array:
        print(ele)


def loggin_config():
    logging.basicConfig(filename="application.logs",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s():%(lineno)d- %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger("application")
    return logger

if __name__ == "__main__":
    message = "WELCOME to YT DOWNLOADER"
    try:
        console_width = os.get_terminal_size().columns - 1
    except:
        console_width = 50
    half_csl = (console_width-len(message))//2
    printS(half_csl*"-"+message+half_csl*"-",color="RED")

    logger = loggin_config()

    printS("enter url : ",color="RED",style="BOLD",sep="",end="")
    URL = input("")

    downloader = Downloader(URL, logger)

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
    
    print_array(streams)
    printS("Stream itag (enter the itag of the stream you want to download): ",color="RED",style="BOLD",sep="",end="")
    itag = input()

    printS("Enter the path when you want to save the downloaded file : ",color="RED",style="BOLD",sep="",end="")
    output_path = input()

    printS("What do you want to name the file : ",color="RED",style="BOLD",sep="",end="")
    file_name = input()

    with LoadingAnimation("Downloading... ") as load:
        load.switch_to_spinner() 
        downloader.download_stream(itag=itag,output_path=output_path,filename=file_name)
    printS("finished Downloading succefuly : "+downloader.yt.title+" as "+file_name,color="GREEN")