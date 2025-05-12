import webview

html = None

with open('gui/index.html','r') as f:
    html = f.read()

window = webview.create_window(title="yt videos downloader",url="http://localhost:9999",html=html)


webview.start()