from pytubefix import YouTube
import sys

# Replace with your desired YouTube video URL
video_url = sys.argv[1] 


# arguments to decide which type of download we want
arguments = sys.argv[2:]


# Create a YouTube object
yt = YouTube(video_url)


stream = yt.streams[0]
stream.download()
