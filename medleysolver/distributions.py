from math import log

class ExponentialDist:
    def __init__(self, lamb, conf):
        self.lamb = lamb
        self.count = 0
        self.total = 0
        self.confidence = conf

    def add_sample(self, sample):
        self.total += sample
        self.count += 1
        self.lamb = self.count / self.total

    def add_timeout(self):
        self.add_sample(self.lamb + self.get_cutoff())

    def get_cutoff(self):
        return log(1 - self.confidence) / (-1 * self.lamb)