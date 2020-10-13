import numpy as np, csv, random, tqdm
import time
from collections import OrderedDict
from medleysolver.compute_features import get_features
from medleysolver.constants import SOLVERS, Result, Solved_Problem, SAT_RESULT, UNSAT_RESULT, is_solved, is_error
from medleysolver.distributions import ExponentialDist
from medleysolver.dispatch import run_problem

def execute(problems, output, classifier, time_manager, timeout, extra_time_to_first):
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

        solver, elapsed, result, rewards, time_spent = apply_ordering(prob, order, timeout - (end - start), time_manager, extra_time_to_first)
        solved_prob = Solved_Problem(prob, point, solver, elapsed + (end - start), result, order, time_spent)

        classifier.update(solved_prob, rewards)

        writer.writerow(solved_prob)


def apply_ordering(problem, order, timeout, time_manager, extra_time_to_first):
    elapsed = 0
    rewards = [-1 for _ in SOLVERS] # negative rewards should be ignored. 
    time_spent = []

    budgets = [int(time_manager.get_timeout(solver))+1 for solver in order]

    for i in range(len(budgets)):
        budgets[i] = min(budgets[i], int(timeout - sum(budgets[:i])))

    if sum(budgets) < timeout:
        if extra_time_to_first:
            budgets[0] = budgets[0] + (timeout - sum(budgets))
        else:
            budgets[-1] = budgets[-1] + (timeout - sum(budgets))

    assert(timeout == sum(budgets))

    order = [order[i] for i in range(len(order)) if budgets[i] > 0]

    for i in range(len(order)):
        solver = order[i]
        time_for_solver = int(timeout - elapsed) + 1 if i == len(order) - 1 else budgets[i]
        res = run_problem(solver, SOLVERS[solver], problem, time_for_solver)

        reward = 1 if is_solved(res.result) else 0
        rewards[list(SOLVERS.keys()).index(solver)] = reward
        time_spent.append(res.elapsed)

        elapsed += res.elapsed
        time_manager.update(solver, res.elapsed, timeout, is_solved(res.result), is_error(res.result))
        if elapsed >= timeout or is_solved(res.result) or i == len(order) - 1:
            return solver, elapsed, res.result, rewards, time_spent
