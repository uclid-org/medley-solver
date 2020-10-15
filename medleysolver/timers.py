from medleysolver.distributions import ExponentialDist
from medleysolver.constants import SOLVERS
from sklearn.linear_model import SGDRegressor

class TimerInterface(object):
    def get_timeout(self, solver, times, point):
        raise NotImplementedError
    
    def update(self, solver, time, success, error, point):
        raise NotImplementedError

class Constant(TimerInterface):
    def __init__(self, const):
        self.const = const
    
    def get_timeout(self, solver, times, point):
        return self.const
    
    def update(self, solver, time, timeout, success, error, point):
        pass

class Exponential(TimerInterface):
    def __init__(self, init_lambda, confidence, T):
        self.timers = {solver:ExponentialDist(init_lambda, confidence, T) for solver in SOLVERS}
    
    def get_timeout(self, solver, times, point):
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
    
    def get_timeout(self, solver, times, point):
        # want time based on times for same solver at nearby points
        timer = ExponentialDist(self.init_lambda, self.confidence, self.T)
        for (s, t) in times:
            if s == solver:
                timer.add_sample(t)
        return timer.get_cutoff()
    
    def update(self, solver, time, timeout, success, error, point):
        pass

class SGD(TimerInterface):
    def __init__(self, init_lambda, confidence, T):
        self.fitted = [False for _ in SOLVERS]
        self.models = [SGDRegressor() for _ in SOLVERS]

    def get_timeout(self, solver, times, point):
        if not self.fitted[solver]: return 60
        clf = self.models[solver]
        return clf.predict(point)

    def update(self, solver, time, timeout, success, error, point):
        clf = self.models[solver]
        if self.fitted[solver]:
            clf.partial_fit(point, time)
        else:
            clf.fit(point, time)
        
