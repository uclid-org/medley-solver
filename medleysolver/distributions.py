from math import log
import numpy as np

class ExponentialDist:
    def __init__(self, lamb, conf, T):
        self.lamb = lamb
        self.count = 0
        self.total = 0
        self.confidence = conf
        self.T = T

    def add_sample(self, sample):
        self.total += sample
        self.count += 1
        self.lamb = self.count / self.total

    def add_timeout(self):
        self.add_sample(1/self.lamb + self.get_cutoff())

    def get_cutoff(self):
        return log(1 - self.confidence + np.exp(-1 * self.lamb * self.T)) / (-1 * self.lamb)

class ThompsonDist(object):
    def __init__(self, n, init_a=1, init_b=1):
        """
        init_a (int): initial value of a in Beta(a, b).
        init_b (int): initial value of b in Beta(a, b).
        n      (int): number of arms in multiarmed bandit.
        """
        self.n = n
        self._as = [init_a] * self.n
        self._bs = [init_b] * self.n

    @property
    def estimated_probas(self):
        return [self._as[i] / (self._as[i] + self._bs[i]) for i in range(self.n)]

    def get_choice(self):
        samples = [np.random.beta(self._as[x], self._bs[x]) for x in range(self.n)]
        i = max(range(self.n), key=lambda x: samples[x])
        return i

    def get_ordering(self):
        samples = [np.random.beta(self._as[x], self._bs[x]) for x in range(self.n)]
        order = sorted(list(range(self.n)), key=lambda x: -1 * samples[x])
        return order 

    def update(self, choice, reward):
        """
        didSolve (bool): whether or not previous choice
        """
        self._as[choice] += reward
        self._bs[choice] += (1 - reward)


