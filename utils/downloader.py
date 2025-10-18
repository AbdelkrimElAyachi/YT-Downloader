from pytubefix import YouTube, exceptions as pt_exceptions
from pytubefix.streams import Stream
from typing import List, Optional, Any
from logger import logger
import os

class Downloader:
    def __init__(self, url: str, *args: Any) -> None:
        if not url:
            raise ValueError("No URL provided !!!")
        self.url = url
        try:
            logger.info(f"Creating YouTube object for URL: {url}")
            self.yt = YouTube(url, *args)
        except pt_exceptions.RegexMatchError as e:
            logger.error(f"The provided URL is not a valid youtube URL : {e}")
            raise ValueError(f"The provided URL is not a valid youtube URL") from e
        except pt_exceptions.VideoUnavailable as e:
            logger.error(f"Video unavailable for url {url} Error : {e}")
            raise ValueError(f"Video unavailable for url {url}") from e
        except Exception as e:
            logger.error(f"Unexpected error while creating yt object : {e}")
            raise ValueError(f"Unexpected error while accessing youtube") from e

    @property
    def streams(self):
        if not hasattr(self, "_streams"):
            self._streams = self.yt.streams
        return self._streams
    
    def get_streams(self, only_audio=False, only_video=False, progressive=False) -> List[Stream]:
        try:
            return list(self.streams.filter(only_audio=only_audio, only_video=only_video, progressive=progressive))
        except Exception as e:
            logger.error(f"Failed to get streams {e}")
            return []
        
    def download_stream(self, itag: int, output_path: Optional[str] = None, filename: Optional[str] = None) -> Optional[str]:
        if itag is None:
            msg = "No itag provided. Please specify a stream itag to download"
            logger.error(msg)
            raise ValueError(msg)
        try:
            stream = self.streams.get_by_itag(itag)
            if not stream:
                msg = f"No stream found with itag: {itag}"
                logger.error(msg)
                raise ValueError(msg)

           # Determine extension from stream
            ext = stream.subtype  # e.g., "mp4" or "webm"
                
            if filename and not filename.endswith(f".{ext}"):
                filename = f"{filename}.{ext}"
            elif not filename:
                filename = stream.default_filename

            if not output_path:
                output_path = os.getcwd() 

            os.makedirs(output_path, exist_ok=True)
                
            logger.info(f"Downloading stream with itag {itag} : ({stream.resolution or stream.abr})")
            file_path = stream.download(output_path=output_path, filename=filename)
            logger.info(f"Download complete: {file_path}")
            return file_path
            
        except Exception as e:
            msg = f"Download failed for itag {itag}: {e}"
            logger.error(msg)
            raise RuntimeError(msg) from e
    
    def get_streams_info(self) -> List[dict]:
        streams_info = []

        all_streams = (
            self.get_streams(only_audio=True) +
            self.get_streams(only_video=True)
        )

        for stream in all_streams:

            if stream.includes_audio_track and not stream.includes_video_track:
                stream_type = "audio"
            elif stream.includes_video_track and not stream.includes_audio_track:
                stream_type = "video"
            else:
                stream_type = "unknown"

            stream_size_mb = round(stream.filesize / (1024*1024), 2) if stream.filesize else 0
            stream_resolution = getattr(stream, "resolution", None)
            stream_abr = getattr(stream, 'abr', None)

            streams_info.append({
                    "itag": stream.itag,
                    "type": stream_type,
                    "size": stream_size_mb,
                    "resolution": stream_resolution,
                    "abr": stream_abr
                })
        return streams_info
