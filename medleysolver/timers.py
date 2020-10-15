from medleysolver.distributions import ExponentialDist
from medleysolver.constants import SOLVERS, ERROR_RESULT, SAT_RESULT, UNSAT_RESULT
from sklearn.linear_model import SGDRegressor
from medleysolver.dispatch import output2result

import csv

class TimerInterface(object):
    def get_timeout(self, solver, position, problem, point):
        raise NotImplementedError
    
    def update(self, solver, time, success, error, point):
        raise NotImplementedError

class Constant(TimerInterface):
    def __init__(self, const):
        self.const = const
    
    def get_timeout(self, solver, position, problem, point):
        return self.const
    
    def update(self, solver, time, timeout, success, error, point):
        pass

class Exponential(TimerInterface):
    def __init__(self, init_lambda, confidence, T):
        self.timers = {solver:ExponentialDist(init_lambda, confidence, T) for solver in SOLVERS}
    
    def get_timeout(self, solver, position, problem, point):
        return self.timers[solver].get_cutoff()
    
    def update(self, solver, time, timeout, success, error, point):
        assert(not success or not error)
        if success: 
            self.timers[solver].add_sample(time)
        else:
            if error:
                self.timers[solver].add_error()
            else:
                self.timers[solver].add_timeout()

class NearestExponential(TimerInterface):
    def __init__(self, init_lambda, confidence, T):
        self.init_lambda = init_lambda
        self.confidence = confidence
        self.T = T
        self.naughtylist = set()
    
    def get_timeout(self, solver, times, problem, point):
        if solver in self.naughtylist:
            return 0
        # want time based on times for same solver at nearby points
        timer = ExponentialDist(self.init_lambda, self.confidence, self.T)
        for (s, t) in times:
            if s == solver:
                timer.add_sample(t)
        return timer.get_cutoff()
    
    def update(self, solver, time, timeout, success, error, point):
        assert(not success or not error)
        if error:
            self.naughtylist.add(solver)

class SGD(TimerInterface):
    def __init__(self, init_lambda, confidence, T):
        self.fitted = [False for _ in SOLVERS]
        self.models = [SGDRegressor() for _ in SOLVERS]

    def get_timeout(self, solver, times, problem, point):
        if not self.fitted[solver]: return 60
        clf = self.models[solver]
        return clf.predict(point)

    def update(self, solver, time, timeout, success, error, point):
        clf = self.models[solver]
        if self.fitted[solver]:
            clf.partial_fit(point, time)
        else:
            clf.fit(point, time)

class PerfectTimer(TimerInterface):
    def get_timeout(self, solver, position, problem, point):
        instance = problem.split("/")[-1]
        directory = problem[:-len(instance)]
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
            elapsed  = 0

        time = elapsed+1 if output == SAT_RESULT or output == UNSAT_RESULT else 0

        return time
    
    def update(self, solver, time, timeout, success, error):
        pass
