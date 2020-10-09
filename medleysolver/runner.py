import numpy as np, csv, random, tqdm
import time
from collections import OrderedDict
from medleysolver.compute_features import get_features
from medleysolver.constants import SOLVERS, Result, Solved_Problem, SAT_RESULT, UNSAT_RESULT, is_solved
from medleysolver.distributions import ExponentialDist
from medleysolver.dispatch import run_problem

def execute(problems, output, classifier, time_manager, timeout):
    mean = 0
    writer = csv.writer(open(output, 'w'))

    for c, prob in tqdm.tqdm(enumerate(problems, 1)): 
        start = time.time()
        point = np.array(get_features(prob))
        #normalizing point
        mean = (c - 1) / c * mean + 1 / c * point
        point = point / (mean+1e-9)

        order = classifier.get_ordering(point, c)
        end = time.time()
        solver, elapsed, result, rewards = apply_ordering(prob, order, timeout - (end - start), time_manager)
        solved_prob = Solved_Problem(prob, point, solver, elapsed + (end - start), result)

        classifier.update(solved_prob, rewards)

        writer.writerow(solved_prob)


def apply_ordering(problem, order, timeout, time_manager):
    elapsed = 0
    rewards = [-1 for _ in SOLVERS] # negative rewards should be ignored. 
    for solver in order:
        if solver == order[-1]:
            time_for_solver = timeout - elapsed
        else:
            time_for_solver = time_manager.get_timeout(solver)
        
        res = run_problem(solver, SOLVERS[solver], problem, time_for_solver)

        reward = (1 - res.elapsed / timeout) ** 4 if is_solved(res.result) else 0
        rewards[list(SOLVERS.keys()).index(solver)] = reward

        elapsed += res.elapsed
        time_manager.update(solver, res.elapsed, is_solved(res.result))
        if elapsed >= timeout or is_solved(res.result):
            break

    return solver, elapsed, res.result, rewards
