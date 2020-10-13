from medleysolver.distributions import ExponentialDist
from medleysolver.constants import SOLVERS

class TimerInterface(object):
    def get_timeout(self, solver, position):
        raise NotImplementedError
    
    def update(self, solver, time, success, error):
        raise NotImplementedError

class Constant(TimerInterface):
    def __init__(self, const):
        self.const = const
    
    def get_timeout(self, solver, position):
        return self.const
    
    def update(self, solver, time, timeout, success, error):
        pass

class Exponential(TimerInterface):
    def __init__(self, init_lambda, confidence):
        self.timers = {solver:ExponentialDist(init_lambda, confidence) for solver in SOLVERS}
    
    def get_timeout(self, solver, position):
        return self.timers[solver].get_cutoff()
    
    def update(self, solver, time, timeout, success, error):
        assert(not success or not error)
        if success: 
            self.timers[solver].add_sample(time)
        else:
            if error:
                self.timers[solver].add_error()
            else:
                self.timers[solver].add_timeout()

class NearestExponential(TimerInterface):
    def __init__(self, init_lambda, confidence):
        self.init_lambda = init_lambda
        self.confidence = confidence
    
    def get_timeout(self, solver, times):
        # want time based on times for same solver at nearby points
        timer = ExponentialDist(self.init_lambda, self.confidence)
        for (s, t) in times:
            if s == solver:
                timer.add_sample(t)
        return timer.get_cutoff()
    
    def update(self, solver, time, timeout, success, error):
        pass
