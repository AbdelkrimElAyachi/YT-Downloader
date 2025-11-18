import ffmpeg
import os

def merge_video_audio(input_video_file, input_audio_file, output_path):
    """
    Merge video and audio, copying video and re-encoding audio if needed
    based on the video container.
    """

    # Determine the video extension
    ext = os.path.splitext(input_video_file)[1].lower()

    # Choose audio codec based on container
    if ext in ['.mp4', '.mov']:
        audio_codec = 'aac'       # MP4-compatible audio
        audio_bitrate = '192k'
    elif ext in ['.webm', '.mkv']:
        audio_codec = 'libopus'   # WebM/MKV-compatible audio
        audio_bitrate = '128k'
    else:
        # fallback: just copy audio (might fail if incompatible)
        audio_codec = 'copy'
        audio_bitrate = None


    # Merge streams with -shortest to handle length mismatch
    ffmpeg.output(
        ffmpeg.input(input_video_file).video,
        ffmpeg.input(input_audio_file).audio,
        output_path,
        vcodec= 'copy',  # always copy video
        acodec= audio_codec,
        audio_bitrate= audio_bitrate,
        shortest=None
    ).run(overwrite_output=True)

    return output_path

