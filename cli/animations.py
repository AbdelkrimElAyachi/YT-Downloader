import threading
import time
import sys
import os
from typing import Optional
from queue import Queue

class LoadingAnimation:
    def __init__(self, message: Optional[str] = None):
        self.message = message or ""
        self._stop_event = threading.Event()
        self._progress_queue = Queue()
        self._current_mode = "spinner"  # or "progress"
        self._current_percent = 0
        self._spinner_steps = ["|", "/", "-", "\\"]
        
        try:
            self.console_width = os.get_terminal_size().columns - 1
        except:
            self.console_width = 50
            
        self.bar_width = self.console_width - len(self.message) - 10  # Account for % display

    def _animation_thread(self):
        spinner_pos = 0
        while not self._stop_event.is_set():
            if self._current_mode == "spinner":
                # Spinner animation
                step = self._spinner_steps[spinner_pos % len(self._spinner_steps)]
                line = f"\r{self.message} {step}"
                spinner_pos += 1
            else:
                # Progress bar animation
                filled = int((self.bar_width * self._current_percent) // 100)
                bar = '[' + "="*filled + ' '*(self.bar_width-filled) + ']'
                line = f"\r{self.message} {bar} {self._current_percent}%"
            
            sys.stdout.write(line)
            sys.stdout.flush()
            time.sleep(0.1)

            # Check for mode/percent updates
            self._process_updates()

    def _process_updates(self):
        """Check for pending updates from the queue"""
        while not self._progress_queue.empty():
            update = self._progress_queue.get_nowait()
            if isinstance(update, str):
                self._current_mode = update  # "spinner" or "progress"
            elif isinstance(update, int):
                self._current_percent = update
            self._progress_queue.task_done()

    def start(self):
        """Start the animation thread"""
        self._stop_event.clear()
        self.thread = threading.Thread(target=self._animation_thread)
        self.thread.daemon = True
        self.thread.start()

    def switch_to_spinner(self):
        """Switch to spinner mode"""
        self._progress_queue.put("spinner")

    def switch_to_progress(self):
        """Switch to progress mode"""
        self._progress_queue.put("progress")
        self._progress_queue.put(max(0, min(100, 0)))

    def update_progress(self, percent: int):
        """Update the progress percentage and switch to progress mode"""
        self._progress_queue.put("progress")
        self._progress_queue.put(max(0, min(100, percent)))

    def stop(self):
        """Stop the animation"""
        self._stop_event.set()
        if self.thread.is_alive():
            self.thread.join()
        sys.stdout.write("\n")
        sys.stdout.flush()

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()
