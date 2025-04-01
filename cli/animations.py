import sys
import time
import os
from typing import Optional 
import threading

class LoadingAnimation:
    def __init__(self,message: Optional[str]):
        self.message = message
        self._stop_event = threading.Event()
        try:
            self.console_width = os.get_terminal_size().columns - 1
        except:
            self.console_width = 50
        self.bar_width = self.console_width - len(message)

    def on_progress_spinner(self, steps=["|","/","-","\\","|"], duration=1, stop=False):
        max_length = max(len(s) for s in steps)
        length = len(steps)
        for i in range(length):
            if stop:
                break
            current = steps[i%length]
            padded = current.ljust(max_length)
            sys.stdout.write(f"\r{padded}")
            sys.stdout.flush()
            time.sleep(duration / length)

    def on_progress_loading(self, percent):
        if self._stop_event.is_set():
            return False
        # [ and ] and the two spaces between message and bar and bar and message and the 4 characters of percent = 8
        filled = int(((self.bar_width-9)* percent)//100)

        bar = '[' + "="*filled + ']'
        percent = str(percent).rjust(3)

        line = f"\r{self.message} {bar}{percent}%"
        line = line[:self.console_width]

        sys.stdout.write(line)
        sys.stdout.flush()
    
    def run_spinner(self):
        self._stop_event.clear()
        self.thread = threading.Thread(target=self.on_progress_spinner)
        self.thread.daemon = True
        self.thread.start()

    def run_loading(self):
        self._stop_event.clear()
        self.thread = threading.Thread(target=self.on_progress_loading)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self._stop_event.set()

    def on_finish(self,message):
        sys.stdout.write("\n FInished succefully\n")
    

