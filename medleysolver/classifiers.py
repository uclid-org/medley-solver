import numpy as np, random, dill
from collections import OrderedDict
from sklearn.neural_network import MLPClassifier
from medleysolver.constants import SOLVERS, is_solved
from medleysolver.distributions import ThompsonDist

class ClassifierInterface(object):
    def get_ordering(self, point, count):
        raise NotImplementedError

    def update(self, solved_prob, rewards):
        raise NotImplementedError

    def save(self, filename):
        with open(filename, "wb") as f:
            dill.dump(self, f)

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

        ordering = np.random.choice(list(SOLVERS.keys()), size=len(SOLVERS), replace=False, p=self.p)
        return list(ordering)
    
    def update(self, solved_prob, rewards):
        for i, reward in enumerate(rewards):
            if reward >= 0:
                reward = reward / self.p[i]
                self.w[i] = self.w[i] * np.exp(self.gamma * reward / len(SOLVERS))

class MLP(ClassifierInterface):
    def __init__(self):
        self.clf = MLPClassifier()
        self.fitted = False

    def get_ordering(self, point, count):
        point = np.array(point).reshape(1, -1)
        if self.fitted:
            choice = self.clf.predict(point)
            order = [list(SOLVERS.keys())[int(choice)]]
        else: 
            order = []
        remaining = [x for x in SOLVERS.keys() if x not in order]
        random.shuffle(remaining)
        order = order + remaining
        return order

    def update(self, solved_prob, rewards):
        X = np.array(solved_prob.datapoint).reshape(1, -1)
        y = np.array([list(SOLVERS.keys()).index(solved_prob.solve_method)])
        if self.fitted:
            self.clf.partial_fit(X, y)
        else:
            self.clf.partial_fit(X, y, classes=np.unique(list(range(len(SOLVERS)))))
        self.fitted = True

class Thompson(ClassifierInterface):
    def __init__(self):
        self.dist = ThompsonDist(len(SOLVERS))
    
    def get_ordering(self, point, count):
        t_order = self.dist.get_ordering()
        order = [list(SOLVERS.keys())[int(choice)] for choice in t_order]
        return order
    
    def update(self, solved_prob, rewards):
        for i, r in enumerate(rewards):
            if r >= 0:
                self.dist.update(i, r)

class LinearBandit(ClassifierInterface):
    def __init__(self, alpha=2.358):
        self.initialized = False
        self.alpha = alpha

    def initialize(self, d):
        self.A_0 = np.identity(d)
        self.B_0 = np.zeros((d, 1))
        self.As = [np.identity(d) for _ in SOLVERS]
        self.Bs = [np.zeros((d, 1)) for _ in SOLVERS]
        self.Cs = [np.zeros((d, d)) for _ in SOLVERS]

    def get_ordering(self, point, count):
        if not self.initialized:
            self.initialize(len(point))
        point = point.reshape((len(point), 1))
        beta = np.linalg.inv(self.A_0) @ self.B_0
        thetas = [np.linalg.inv(self.As[i]) @ (self.Bs[i] - self.Cs[i] @ beta) for i in range(len(SOLVERS))]
        sigmas = [point.T @ np.linalg.inv(self.A_0) @ point - 2 * point.T @ \
                np.linalg.inv(self.A_0) @ self.Cs[i].T @ np.linalg.inv(self.As[i]) @ point \
                + point.T @ np.linalg.inv(self.As[i]) @ point + point.T @ \
                np.linalg.inv(self.As[i]) @ self.Cs[i] @ np.linalg.inv(self.A_0) @ self.Cs[i].T @ np.linalg.inv(self.As[i]) @ point\
                for i in range(len(SOLVERS))]
        
        ps = [thetas[i].T @ point + beta.T @ point + self.alpha * np.sqrt(sigmas[i]) for i in range(len(SOLVERS))]
        choice = np.random.choice(np.flatnonzero(np.isclose(ps, max(ps)))) #running argmax while arbitrarily breaking ties

        order = [list(SOLVERS.keys())[int(choice)]]
        remaining = [x for x in SOLVERS.keys() if x not in order]
        random.shuffle(remaining)
        order = order + remaining
        return order

    def update(self, solved_prob, rewards):
        point = solved_prob.datapoint.reshape((len(solved_prob.datapoint), 1))
        for i, r in enumerate(rewards):
            if r >= 0:
                self.A_0 += self.Cs[i].T @ np.linalg.inv(self.As[i]) @ self.Cs[i]
                self.B_0 += self.Cs[i].T @ np.linalg.inv(self.As[i]) @ self.Bs[i]
                self.As[i] = self.As[i] + point @ point.T
                self.Bs[i] = self.Bs[i] + r * point
                self.Cs[i] = self.Cs[i] + point @ point.T
                self.A_0 += point @ point.T - self.Cs[i].T @ np.linalg.inv(self.As[i]) @ self.Cs[i]
                self.B_0 += r * point - self.Cs[i].T @ np.linalg.inv(self.As[i]) @ self.Bs[i]


class Preset(ClassifierInterface):
    def __init__(self, solver):
        self.solver = solver
    
    def get_ordering(self, point, count):
        return [self.solver]
    
    def update(self, solved_prob, rewards):
        pass
