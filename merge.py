import ffmpeg


def merge_video_and_audio(video_path, audio_path):
    # Input files
    video_input = ffmpeg.input(video_path)
    audio_input = ffmpeg.input(audio_path)

    # Merge and output
    ffmpeg.output(
        video_input, audio_input,
        'merged_video.mp4',
        vcodec='vp9',  # Keep original video codec = vp9
        acodec='aac'   # Keep original audio codec = mp4a.40.5
    ).run(overwrite_output=True)  # Overwrite if file exists

merge_video_and_audio("song.webm", "song.mp4")