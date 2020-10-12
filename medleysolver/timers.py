from medleysolver.distributions import ExponentialDist
from medleysolver.constants import SOLVERS

class TimerInterface(object):
    def get_timeout(self, solver):
        raise NotImplementedError
    
    def update(self, solver, time, success):
        raise NotImplementedError

class Constant(TimerInterface):
    def __init__(self, const):
        self.const = const
    
    def get_timeout(self, solver):
        return self.const
    
    def update(self, solver, time, success):
        pass

class Exponential(TimerInterface):
    def __init__(self, init_lambda, confidence):
        self.timers = {solver:ExponentialDist(init_lambda, confidence) for solver in SOLVERS}
    
    def get_timeout(self, solver):
        return self.timers[solver].get_cutoff()
    
    def update(self, solver, time, success, error):
        assert(not success or not error)
        if success: 
            self.timers[solver].add_sample(time)
        else:
            if error:
                self.timers[solver].add_error()
            else:
                self.timers[solver].add_timeout()

