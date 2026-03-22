import ffmpeg
from typing import Optional
from logger import logger


def get_codecs(filename: str) -> dict:
    """
    Probe a media file and return its video codec, audio codec, and container format.

    Args:
        filename: Path to the media file to probe.

    Returns:
        A dict with keys 'vcodec', 'acodec', and 'container'.
    """
    try:
        probe = ffmpeg.probe(filename)
    except ffmpeg.Error as e:
        logger.error(f"Failed to probe file '{filename}': {e}")
        return {"vcodec": None, "acodec": None, "container": None}

    video_stream = next((s for s in probe['streams'] if s['codec_type'] == 'video'), None)
    audio_stream = next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)

    return {
        "vcodec": video_stream['codec_name'] if video_stream else None,
        "acodec": audio_stream['codec_name'] if audio_stream else None,
        "container": probe['format']['format_name'],
    }