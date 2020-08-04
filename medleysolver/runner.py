import numpy as np, csv, random
from collections import OrderedDict
from medleysolver.compute_features import get_features
from medleysolver.constants import SOLVERS, Result, Solved_Problem, SAT_RESULT, UNSAT_RESULT, is_solved
from medleysolver.distributions import ExponentialDist
from medleysolver.dispatch import run_problem

def execute(problems, output, classifier, time_manager, timeout):
    mean = 0
    writer = csv.writer(open(output, 'wb'))

    for c, prob in enumerate(problems, 1): 
        point = np.array(get_features(prob))
        #normalizing point
        mean = (c - 1) / c * mean + 1 / c * point
        point = point / mean

        order = classifier.get_ordering(point, c)

        solver, elapsed, result = apply_ordering(prob, order, timeout, time_manager)
        solved_prob = Solved_Problem(prob, point, solver, elapsed, result)

        classifier.update(solved_prob)

        writer.writerow(solved_prob)


def apply_ordering(problem, order, timeout, time_manager):
    elapsed = 0

    for solver in order:
        if solver == order[-1]:
            res = run_problem(solver, SOLVERS[solver], problem, timeout - elapsed)
        else:
            res = run_problem(solver, SOLVERS[solver], problem, time_manager.get_timeout(solver))
        
        elapsed += res.elapsed
        time_manager.update(solver, res.elapsed, is_solved(res.result))
        if elapsed >= timeout or is_solved(res.result):
            break

    return solver, elapsed, res.result
