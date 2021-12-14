import time


class Timer():
    def __init__(self, t=400):
        self.initial_t = round(time.time())
        self.last = None
        self.t = t

    def update(self):
        if self.last != round(time.time()):
            self.t -= round(time.time()) - self.initial_t - (400 - self.t)
            self.last = round(time.time())