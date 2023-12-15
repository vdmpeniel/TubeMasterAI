import time


class Telemetry:

    def __init__(self):
        self.start_time = -1
        self.elapsed_time = -1

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.elapsed_time = time.time() - self.start_time
        return self.elapsed_time

    def reset(self):
        self.start_time = -1
        self.elapsed_time = -1
        return
