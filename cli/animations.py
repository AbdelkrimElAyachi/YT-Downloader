import sys
import time
import os
from typing import Optional 

def iterativeAnimation(loops=1,steps=["|","/","-","\\","|"],duration=1):
    max_length = max(len(s) for s in steps)
    length = len(steps)
    for i in range(loops * length):
        current = steps[i%length]
        padded = current.ljust(max_length)
        sys.stdout.write(f"\r{padded}")
        sys.stdout.flush()
        time.sleep(duration / length)
    print("\n")

class LoadingAnimation:
    def __init__(self,message: Optional[str]):
        self.message = message
        try:
            self.console_width = os.get_terminal_size().columns - 1
        except:
            self.console_width = 50
        self.bar_width = self.console_width - len(message)


    def on_progress(self, percent):
        # [ and ] and the two spaces between message and bar and bar and message and the 4 characters of percent = 8
        filled = int(((self.bar_width-9)* percent)//100)

        bar = '[' + "="*filled + ']'
        percent = str(percent).rjust(3)

        line = f"\r{self.message} {bar}{percent}%"
        line = line[:self.console_width]

        sys.stdout.write(line)
        sys.stdout.flush()

    def on_finish(self,message):
        sys.stdout.write("\n FInished succefully\n")

iterativeAnimation()