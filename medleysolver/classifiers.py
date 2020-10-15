import numpy as np, random, dill
from collections import OrderedDict
from sklearn.neural_network import MLPClassifier
from medleysolver.constants import SOLVERS, is_solved, ERROR_RESULT
from medleysolver.distributions import ThompsonDist
from more_itertools import unique_everseen
from medleysolver.dispatch import output2result

import csv 

class ClassifierInterface(object):
    def __init__(self, time_k):
        self.time_k = time_k
        self.solved = []

    def get_ordering(self, point, count, problem):
        raise NotImplementedError

    def get_nearby_times(self, point, count):
        positions = sorted(self.solved, key=lambda entry: np.linalg.norm(entry.datapoint - point))[:self.time_k]
        positions = [(x.solve_method, x.time) for x in positions]
        return positions

    def update(self, solved_prob, rewards):
        #TODO: Implement pruning
        if is_solved(solved_prob.result):
            self.solved.append(solved_prob)

    def save(self, filename):
        with open(filename, "wb") as f:
            dill.dump(self, f)

class Random(ClassifierInterface):
    def get_ordering(self, point, count, problem):
        order = list(SOLVERS.keys())
        np.random.shuffle(order)
        return order


class NearestNeighbor(ClassifierInterface):
    def __init__(self, epsilon, decay, kind, time_k):
        self.solved = []
        self.epsilon = epsilon
        self.decay = decay
        self.counter = 0
        self.kind = kind
        super(NearestNeighbor, self).__init__(time_k)
    
    def get_ordering(self, point, count, problem):
        if self.kind == "greedy":
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
                order = Random.get_ordering(self, point, count, problem)
        elif self.kind == "single":
            if np.random.rand() >= self.epsilon * (self.decay ** count) and self.solved:
                #first sort based on distance to inputted point
                candidate = sorted(self.solved, key=lambda entry: np.linalg.norm(entry.datapoint - point))[0]
                order = list(OrderedDict((x.solve_method, True) for x in [candidate]).keys())
                remaining = [x for x in SOLVERS.keys() if x != candidate]
                random.shuffle(remaining)
                order = order + remaining
            else:
                order = Random.get_ordering(self, point, count, problem)
        else:
            candidate = sorted(self.solved, key=lambda entry: np.linalg.norm(entry.datapoint - point))
            order = list(OrderedDict((x.solve_method, True) for x in candidate).keys())
            remaining = [x for x in SOLVERS.keys() if x not in order]
            np.random.shuffle(remaining)
            order = order + remaining

        return list(unique_everseen(order))

    
class Exp3(ClassifierInterface):
    def __init__(self, gamma, time_k):
        self.gamma = gamma
        self.w = [1 for _ in SOLVERS]
        self.p = [0 for _ in SOLVERS]
        super(Exp3, self).__init__(time_k)
    
    def get_ordering(self, point, count, problem):
        for i, _ in enumerate(SOLVERS):
            self.p[i] = (1-self.gamma) * self.w[i] / sum(self.w) + self.gamma / len(SOLVERS)

        ordering = np.random.choice(list(SOLVERS.keys()), size=len(SOLVERS), replace=False, p=self.p)
        return list(unique_everseen(ordering))
    
    def update(self, solved_prob, rewards):
        for i, reward in enumerate(rewards):
            if reward >= 0:
                reward = reward / self.p[i]
                self.w[i] = self.w[i] * np.exp(self.gamma * reward / len(SOLVERS))

        #TODO: Implement pruning
        if is_solved(solved_prob.result):
            self.solved.append(solved_prob)

class MLP(ClassifierInterface):
    def __init__(self, time_k):
        self.clf = MLPClassifier()
        self.fitted = False
        super(MLP, self).__init__(time_k)

    def get_ordering(self, point, count, problem):
        point = np.array(point).reshape(1, -1)
        if self.fitted:
            scores = self.clf.predict_proba(point)
            order = sorted(list(range(len(SOLVERS))), key=lambda x: -1 * scores[x])
            choice = self.clf.predict(point)
            order = [list(SOLVERS.keys())[int(choice)]]
        else: 
            order = []
        remaining = [x for x in SOLVERS.keys() if x not in order]
        np.random.shuffle(remaining)
        order = order + remaining
        return list(unique_everseen(order))

    def update(self, solved_prob, rewards):
        X = np.array(solved_prob.datapoint).reshape(1, -1)
        y = np.array([list(SOLVERS.keys()).index(solved_prob.solve_method)])
        if self.fitted:
            self.clf.partial_fit(X, y)
        else:
            self.clf.partial_fit(X, y, classes=np.unique(list(range(len(SOLVERS)))))
        self.fitted = True

        #TODO: Implement pruning
        if is_solved(solved_prob.result):
            self.solved.append(solved_prob)

class Thompson(ClassifierInterface):
    def __init__(self, kind, time_k):
        self.dist = ThompsonDist(len(SOLVERS))
        self.kind = kind
        super(Thompson, self).__init__(time_k)
    
    def get_ordering(self, point, count, problem):
        if self.kind == "single":
            t_order = self.dist.get_ordering()
            order = [[list(SOLVERS.keys())[int(choice)] for choice in t_order][0]]
            remaining = [x for x in SOLVERS.keys() if x not in order]
            random.shuffle(remaining)
            order = order + remaining
        else:
            t_order = self.dist.get_ordering()
            order = [list(SOLVERS.keys())[int(choice)] for choice in t_order]
        return list(unique_everseen(order))
    
    def update(self, solved_prob, rewards):
        for i, r in enumerate(rewards):
            if r > 0:
                self.dist.update(i, 1)
            elif r == 0:
                self.dist.update(i, 0)
            else:
                pass
        if is_solved(solved_prob.result):
            self.solved.append(solved_prob)

class LinearBandit(ClassifierInterface):
    def __init__(self, time_k, alpha=2.358):
        self.initialized = False
        self.alpha = alpha
        super(LinearBandit, self).__init__(time_k)

    def initialize(self, d):
        self.A_0 = np.identity(d)
        self.B_0 = np.zeros((d, 1))
        self.As = [np.identity(d) for _ in SOLVERS]
        self.Bs = [np.zeros((d, 1)) for _ in SOLVERS]
        self.Cs = [np.zeros((d, d)) for _ in SOLVERS]

    def get_ordering(self, point, count, problem):
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
        ss = list(range(len(ps)))
        np.random.shuffle(ss)
        i_order = sorted(ss, key=lambda x: -1 * ps[x])
        order = [list(SOLVERS.keys())[int(choice)] for choice in i_order]
        return list(unique_everseen(order))

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

        #TODO: Implement pruning
        if is_solved(solved_prob.result):
            self.solved.append(solved_prob)


class Preset(ClassifierInterface):
    def __init__(self, solver):
        self.solver = solver
    
    def get_ordering(self, point, count, problem):
        return [self.solver]
    
    def update(self, solved_prob, rewards):
        pass

class PerfectSelector(ClassifierInterface):
    
    def get_ordering(self, point, count, problem):

        instance = problem.split("/")[-1]
        directory = problem[:-len(instance)]

        time_solver = {s:60 for s in SOLVERS}

        for solver in SOLVERS:
            try:
                with open(directory+"/"+solver+".csv") as csvfile:
                    results = list(csv.reader(csvfile))
                    results = list(filter(lambda s: s[0] == problem, results))
                    assert(len(results) == 1)
                    output = results[0][4]
                    output = output2result(problem, output)
                    elapsed = float(results[0][3])
            except:
                output   = ERROR_RESULT,
                elapsed  = 60

            time_solver[solver] = elapsed if output != ERROR_RESULT else 60

        sorted_solvers = sorted(time_solver.keys(), key=lambda x: time_solver[x])
        return sorted_solvers

class KNearest(ClassifierInterface):
    def __init__(self, k, epsilon, decay, time_k):
        self.k = k
        self.epsilon = epsilon
        self.decay = decay
        self.solved = []
        self.counter = 0
        super(KNearest, self).__init__(time_k)

    def get_ordering(self, point, count, problem):
        if np.random.rand() >= self.epsilon * (self.decay ** count) and self.solved:
            candidates = sorted(self.solved, key=lambda entry: np.linalg.norm(entry.datapoint - point))[:self.k]
            methods = [x.solve_method for x in candidates]
            ss = list(SOLVERS.keys())
            np.random.shuffle(ss)
            order = sorted(ss, key= lambda x: -1 * methods.count(x))
        else:
            order = Random.get_ordering(self, point, count, problem)
        return order