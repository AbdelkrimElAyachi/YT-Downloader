import ffmpeg

def get_codecs(filename):
    # Probe the file metadata
    probe = ffmpeg.probe(filename)
    
    # Extract video and audio streams
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
    
    # Get codec names
    vcodec = video_stream['codec_name'] if video_stream else None
    acodec = audio_stream['codec_name'] if audio_stream else None
    
    return {
        "vcodec": vcodec,  # e.g., "h264", "vp9", "av1"
        "acodec": acodec,  # e.g., "aac", "opus", "mp3"
        "container": probe['format']['format_name']  # e.g., "mp4", "webm"
    }

# Example usage
#file_info = get_codecs("your_file.mp4")
#print("Video Codec:", file_info["vcodec"])
#print("Audio Codec:", file_info["acodec"])
#print("Container:", file_info["container"])