from MyYoutube import MyYoutube
from prompt import multiple_choices,Loader



print("----------------------------- Youtube Downloader ------------------------")
url = input("the video url : ")
download_type = multiple_choices("what do you want to download",["video","audio"])

# Create a YouTube object
video = MyYoutube(url)

streams = video.streams.filter(type=download_type)

if streams is None:
    print("no streams were found")

for stream in streams:
    print(stream)

stream_itag = input("enter the itag of the stream you want to download : ")

chosen_stream = streams.get_by_itag(stream_itag)

loader = Loader()
loader.start()
chosen_stream.download()
loader.end()


print(video.title + "was downloaded succefully")

