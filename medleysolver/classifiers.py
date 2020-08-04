import numpy as np, random
from collections import OrderedDict
from medleysolver.constants import SOLVERS, is_solved

class ClassifierInterface(object):
    def get_ordering(self, point, count):
        raise NotImplementedError

    def update(self, solved_prob, rewards):
        raise NotImplementedError

class Random(ClassifierInterface):
    def get_ordering(self, point, count):
        order = list(SOLVERS.keys())
        random.shuffle(order)
        return order
    
    def update(self, solved_prob, rewards):
        return


class NearestNeighbor(ClassifierInterface):
    def __init__(self, epsilon, decay):
        self.solved = []
        self.epsilon = epsilon
        self.decay = decay
        self.counter = 0
    
    def get_ordering(self, point, count):
        if np.random.rand() >= self.epsilon * (self.decay ** count) and self.solved:
            #first sort based on distance to inputted point
            candidates = sorted(self.solved, key=lambda entry: np.linalg.norm(entry.datapoint - point))[:len(self.solved) // 10 + 1]
            #extract most similar 10%, resort based on speed
            fast = sorted(candidates, key=lambda entry: entry.time)
            order = list(OrderedDict((x.solve_method, True) for x in fast).keys())
            #randomly append solvers not found in sort
            remaining = [x for x in SOLVERS.keys() if x not in order]
            random.shuffle(remaining)
            order = order + remaining
        else:
            order = Random.get_ordering(self, point, count)

        return order
    
    def update(self, solved_prob, rewards):
        #TODO: Implement pruning
        if is_solved(solved_prob.result):
            self.solved.append(solved_prob)

class Exp3(ClassifierInterface):
    def __init__(self, gamma):
        self.gamma = gamma
        self.w = [1 for _ in SOLVERS]
        self.p = [0 for _ in SOLVERS]
    
    def get_ordering(self, point, count):
        for i, _ in enumerate(SOLVERS):
            self.p[i] = (1-self.gamma) * self.w[i] / sum(self.w) + self.gamma / len(SOLVERS)

        ordering = np.random.choice(SOLVERS.keys(), size=len(SOLVERS), replace=False, p=self.p)
        return list(ordering)
    
    def update(self, solved_prob, rewards):
        for i, reward in enumerate(rewards):
            if reward >= 0:
                reward = reward / self.p[i]
                self.w[i] = self.w[i] * np.exp(self.gamma * reward / len(SOLVERS))

