import time

class Timer:
    def __init__(self) -> None:
        self.start_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        return time.time() - self.start_time
    
    def reset(self):
        self.start_time = 0