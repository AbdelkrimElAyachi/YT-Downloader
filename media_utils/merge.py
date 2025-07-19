import ffmpeg

def merge_video_audio(input_video_file, input_audio_file)

    input_video = ffmpeg.input(input_video_file)  # video file
    input_audio = ffmpeg.input(input_audio_file)  # audio file

    output_path = "./output.mp4"

    ffmpeg.output(input_video.video, input_audio.audio, output_path, vcodec='copy', acodec='copy').run()

    return output_path

