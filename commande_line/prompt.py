import inquirer
import time
import threading

# multiple choices
def multiple_choices(message,choices):
    questions = [
        inquirer.List('option',
                      message=message,
                      choices=choices,
                      ),
    ]
    answers = inquirer.prompt(questions)
    choice = answers['option']

    return choice

class Loader():

    def __init__(self):
        self.loading_symbols = ['|', '/', '-', '\\']
        # Create an event to stop the loading animation
        self.stop_loading = threading.Event()
        pass
    
    # Function to display loading animation
    def loading_animation(self):
        idx = 0
        while not self.stop_loading.is_set():
            print(f'\rLoading... {self.loading_symbols[idx]}', end='', flush=True)
            idx = (idx + 1) % len(self.loading_symbols)
            time.sleep(0.1)

    def start(self):
        # Start the loading animation in a separate thread
        self.loading_thread = threading.Thread(target=self.loading_animation)
        self.loading_thread.start()

    def end(self):
        # Stop the loading animation
        self.stop_loading.set()
        self.loading_thread.join()  # Wait for the thread to finish
        print() # return to new line

