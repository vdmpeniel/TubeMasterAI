import time
import os
os.environ['TERM'] = 'xterm'


class OutputManager:
    def __init__(self):
        self.output_chain = []

    def print_output_chain(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for line in self.output_chain:
            print(f'{line}\n')

    def update_progress_bar(self, bar_length=50, progress=0):
        block = int(round(bar_length * progress / 100))
        progress_str = "[" + "=" * block + " " * (bar_length - block) + "] " + str(int(progress)) + "%"
        print(progress_str)
        time.sleep(0.1)

    def log_message(self, message, progress):
        self.output_chain.append(message)
        self.print_output_chain()
        self.update_progress_bar(progress)
