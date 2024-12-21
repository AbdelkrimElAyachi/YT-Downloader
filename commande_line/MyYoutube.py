from pytubefix import YouTube


class MyYoutube(YouTube):

    def __init__(self,*args):
        try:
            super().__init__(*args)
        except Exception as e:
            print(f"unable to find the video : {e}")

    def download_audio(self):
        pass

    def download_video(self):
        pass


