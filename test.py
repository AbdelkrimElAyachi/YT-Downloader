from utils import Downloader
import webview

# CONSTANTS
PATH = 'gui/index.html'

# api class that has python methods that we will use
class API:
    def set_url(self, url):
        print(f"the url has been set succefully : {url}")
        self.downloader = Downloader(url)
        return True;

    def select_folder(self):
        return None

    def retrieve_video_title(self):
        print(f"the video title")
        return self.downloader.yt.title;

    def retrieve_thumbnail_url(self):
        print(f"the video thumbnail url retrieved succefully")
        return self.downloader.yt.thumbnail_url;

       
class GUI:
    def __init__(self, html, cls):
        self.window = webview.create_window(
                title="yt videos downloader", 
                url="http://localhost:9999", 
                html=html,js_api=cls(), 
                width=500, 
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
