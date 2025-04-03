from pytubefix import YouTube
from pytubefix.streams import Stream
from typing import List, Optional, Union, Any, Dict, Tuple, TypeVar
import logging
from pathlib import Path


class Downloader:
    """
    A wrapper class for pytubefix to download YouTube videos.
    
    Attributes:
        url (str): The YouTube video URL
        yt (YouTube): The pytubefix YouTube object
        logger (logging.Logger): Logger for the class
    """
    
    def __init__(self, url: str, custom_logger: Optional[logging.Logger] = None, *args: Any) -> None:
        """
        Initialize the Downloader with a YouTube URL.
        
        Args:
            url: The YouTube video URL
            custom_logger: Optional custom logger instance
            *args: Additional arguments to pass to YouTube constructor
            
        Raises:
            ValueError: If the URL is invalid or empty
            Error : If the URL is invalid or the connection is not established correctly
        """
        if not url:
            raise ValueError("URL cannot be empty")
        
        self.url = url
        self.logger = custom_logger or logging.getLogger(__name__)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        try:
            self.logger.info(f"Creating YouTube object for URL: {url}")
            self.yt = YouTube(url, *args)
            
        except Exception as e:
            self.logger.error(f"Failed to create YouTube object: {e}")
            raise Error(f"Invalid YouTube URL or connection error: {e}")
    
    def _safe_operation(self, operation: callable, error_message: str, *args, **kwargs) -> Optional:
        """
        Internal method to safely execute operations with proper error handling.
        
        Args:
            operation: Function to execute
            error_message: Error message to log if operation fails
            *args, **kwargs: Arguments to pass to the operation
            
        Returns:
            Result of the operation or None if failed
        """
        try:
            return operation(*args, **kwargs)
        except Exception as e:
            self.logger.error(f"{error_message}: {e}")
            return None
    
    def get_audios_only(self) -> List[Stream]:
        """
        Get all available audio streams.
        
        Returns:
            List of audio streams or empty list if failed
        """
        return self._safe_operation(
            lambda: self.yt.streams.filter(only_audio=True),
            "Failed to retrieve audio streams"
        ) or []
    
    def get_videos(self) -> List[Stream]:
        """
        Get all progressive video streams (with audio).
        
        Returns:
            List of progressive video streams or empty list if failed
        """
        return self._safe_operation(
            lambda: self.yt.streams.filter(progressive=True),
            "Failed to retrieve progressive video streams"
        ) or []
    
    def get_videos_only(self) -> List[Stream]:
        """
        Get video-only streams (no audio).
        
        Returns:
            List of video-only streams or empty list if failed
        """
        return self._safe_operation(
            lambda: self.yt.streams.filter(only_video=True),
            "Failed to retrieve video-only streams"
        ) or []
    
    def download_stream(self, itag: int, output_path: Optional[str] = None, 
                        filename: Optional[str] = None) -> Optional[str]:
        """
        Download a specific stream by its itag.
        
        Args:
            itag: The itag of the stream to download
            output_path: Optional directory to save the file to
            filename: Optional filename (without extension)
            
        Returns:
            Path to downloaded file or None if download failed
        """
        try:
            stream = self.yt.streams.get_by_itag(itag)
            if not stream:
                self.logger.error(f"No stream found with itag: {itag}")
                return None
                
            kwargs = {}
            if output_path:
                kwargs['output_path'] = output_path
            if filename:
                kwargs['filename'] = filename
                
            self.logger.info(f"Downloading stream with itag {itag} ({stream.resolution or stream.abr})")
            file_path = stream.download(**kwargs)
            self.logger.info(f"Download complete: {file_path}")
            return file_path
            
        except Exception as e:
            self.logger.error(f"Download failed for itag {itag}: {e}")
            return None
    
    def get_video_info(self) -> Dict[str, Any]:
        """
        Get basic information about the video.
        
        Returns:
            Dictionary containing video information
        """
        self.logger.debug(f"Fetching video info for {self.url}")
        
        try:
            info = {
                "title": self.yt.title,
                "author": self.yt.author,
                "length": self.yt.length,
                "views": self.yt.views,
                "publish_date": self.yt.publish_date,
                "description": self.yt.description,
                "thumbnail_url": self.yt.thumbnail_url,
                "rating": self.yt.rating
            }
            self.logger.info(f"Retrieved info for video: {info['title']}")
            return info
            
        except Exception as e:
            self.logger.error(f"Error getting video info: {e}")
            return {}
    
    def get_highest_resolution(self) -> Optional[Stream]:
        """
        Get the highest resolution video stream (with audio).
        
        Returns:
            Highest resolution stream or None if no streams available
        """
        videos = self.get_videos()
        return max(videos, key=lambda x: int(x.resolution[:-1]), default=None) if videos else None
    
    def get_best_audio(self) -> Optional[Stream]:
        """
        Get the best quality audio stream.
        
        Returns:
            Highest bitrate audio stream or None if no streams available
        """
        audios = self.get_audios()
        return max(audios, key=lambda x: int(x.abr[:-5]) if x.abr else 0, default=None) if audios else None
    
    def download_highest_resolution(self, output_path: Optional[str] = None) -> Optional[str]:
        """
        Download the highest resolution video available.
        
        Args:
            output_path: Optional directory to save the file to
            
        Returns:
            Path to downloaded file or None if download failed
        """
        stream = self.get_highest_resolution()
        if not stream:
            self.logger.error("No video streams available")
            return None
        
        return self.download_stream(stream.itag, output_path)
    
    def download_best_audio(self, output_path: Optional[str] = None) -> Optional[str]:
        """
        Download the best quality audio available.
        
        Args:
            output_path: Optional directory to save the file to
            
        Returns:
            Path to downloaded file or None if download failed
        """
        stream = self.get_best_audio()
        if not stream:
            self.logger.error("No audio streams available")
            return None
        
        return self.download_stream(stream.itag, output_path)