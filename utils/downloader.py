from pytubefix import YouTube
from pytubefix.streams import Stream
from typing import List, Optional, Any, Callable, Iterable, Tuple 
from utils.logger import logger 


class Downloader:
    """pytubefix YouTube downloader wrapper."""
    
    def __init__(self, url: str, *args: Any) -> None:
        """Init Downloader; raise on invalid URL or connection error."""
        self.streams = None
        if not url:
            return
        self.url = url
        try:
            logger.info(f"Creating YouTube object for URL: {url}")
            self.yt = YouTube(url, *args)
        except Exception as e:
            logger.error(f"Failed to create YouTube object: {e}")
            raise Exception(f"Invalid YouTube URL or connection error: {e}")

    def _get_streams(self) -> Optional[Iterable[Stream]]:
        """Retrieve the streams and cache them in case we need them agains."""
        if self.streams is None:
            try:
                self.streams = self.yt.streams
            except Exception as e:
                logger.error(f"Failed to retrieve streams : {e}")
        return self.streams


    
    def _safe_operation(self, operation: Callable, error_message: str, *args, **kwargs) -> Optional[Any]:
        """Run a callable safely; return None on error."""
        self._get_streams()
        try:
            return operation(*args, **kwargs)
        except Exception as e:
            logger.error(f"{error_message}: {e}")
            return None
    
    def get_audios_only(self) -> List[Stream]:
        """Return all audio streams or empty list if failed."""
        return self._safe_operation(
            lambda: self.streams.filter(only_audio=True),
            "Failed to retrieve audio streams"
        ) or []
    
    def get_videos(self) -> List[Stream]:
        """Return all progressive (video+audio) streams or empty list if failed."""
        return self._safe_operation(
            lambda: self.streams.filter(progressive=True),
            "Failed to retrieve progressive video streams"
        ) or []
    

    def get_videos_only(self) -> List[Stream]:
        """Return video-only streams or empty list if unavailable."""
        return self._safe_operation(
            lambda: self.streams.filter(only_video=True),
            "Failed to retrieve video-only streams"
        ) or []
    

    def download_stream(self, itag: int, output_path: Optional[str] = None, filename: Optional[str] = None) -> Optional[str]:
        """Download stream by itag; return file path or None if failed."""
        try:
            stream = self.streams.get_by_itag(itag)
            if not stream:
                logger.error(f"No stream found with itag: {itag}")
                return None
                
            kwargs = {}
            if output_path:
                kwargs['output_path'] = output_path
            if filename:
                kwargs['filename'] = filename
                
            logger.info(f"Downloading stream with itag {itag} : ({stream.resolution or stream.abr})")
            file_path = stream.download(**kwargs)
            logger.info(f"Download complete: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Download failed for itag {itag}: {e}")
            return None
    
    def get_videos_resolutions(self) -> List[Tuple[int, str, float]]:
        return [
                (stream.itag, stream.resolution, round(stream.filesize / (1024*1024), 2) )
                for stream in self.get_videos_only()
                if stream.resolution is not None
        ]

    def get_audios_bit_rates(self) -> List[Tuple[int, str, float]]:
        return [
                (stream.itag, stream.abr, round(stream.filesize / (1024*1024), 2))
                for stream in self.get_audios_only()
                if stream.abr is not None
        ]
