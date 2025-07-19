import webview
from downloader import Downloader

html = None

with open('gui/index.html','r') as f:
    html = f.read()

window = webview.create_window(title="yt videos downloader",url="http://localhost:9999",html=html,js_api=Downloader())


webview.start()