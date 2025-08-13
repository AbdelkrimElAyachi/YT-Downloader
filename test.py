from ffmpeg import output
from utils import Downloader
from media_utils import merge_video_audio
from os import path
import webview
import tempfile
import re

# CONSTANTS
PATH = 'gui/index.html'

# api class that has python methods that we will use
class API:

    def set_url(self, url):
        print(f"the url has been set succefully : {url}")
        self.downloader = Downloader(url)
        self.title = self.downloader.yt.title
        self.tmpdir = None
        return True;

    def retrieve_video_title(self):
        print(f"the video title retrieved succefully")
        return self.title;

    def retrieve_thumbnail_url(self):
        print(f"the video thumbnail url retrieved succefully")
        return self.downloader.yt.thumbnail_url;

    def retrieve_videos_resolutions(self):
        print(f"video resolutsion retrieved succefully")
        return self.downloader.get_videos_resolutions()

    def retrieve_audio_bit_rates(self):
        print(f"audio bit rates retrieved succefully")
        return self.downloader.get_audios_bit_rates()

    def close(self):
        webview.windows[0].destroy()
        exit(0)

    def download(self, itag, filename):
        if(self.tmpdir is None):
            self.tmpdir = tempfile.TemporaryDirectory()
        return self.downloader.download_stream(itag, self.tmpdir.name, filename)

    def download_directly(self, itag):
        output_path = self.get_save_path()
        if not output_path:
            print("save cancelled")
            return None
        folder = path.dirname(output_path)
        filename = path.basename(output_path)
        return self.downloader.download_stream(itag, folder, filename)

    def get_save_path(self):
        filename = self.sanitize_filename(self.title)
        folder = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG, save_filename=f"{filename}.mp4", file_types = ("MP4 Video (*.mp4)", "All files (*.*)"))
        if folder:
            return folder[0]
        return None

    def merge(self, video_file, audio_file):
        output_path = self.get_save_path()
        if not output_path:
            print("save cancelled")
            return None
        merge_video_audio(video_file, audio_file, output_path)
        self.clean_temporary_files()
        return output_path

    def clean_temporary_files(self):
        if self.tmpdir is not None:
            self.tmpdir.cleanup()
            self.tmpdir = None
            print("temporary files cleaned succefully")

    def sanitize_filename(self,filename):
        # Remove invalid chars for Windows, Linux, Mac
        cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', filename).strip()
        return cleaned[:100]  # Limit length to 100 chars

class GUI:
    def __init__(self, html, cls):
        self.window = webview.create_window(
                title="yt videos downloader", 
                url="http://localhost:9999", 
                html=html,js_api=cls(), 
                width=800, 
                height=500, 
                resizable=False)

    def run(self):
        webview.start()


def read_file(path):
    with open(path,'r') as f:
        html = f.read()
        return html


if __name__ == "__main__":
    html = read_file(PATH)
    app = GUI(html, API)
    app.run()
