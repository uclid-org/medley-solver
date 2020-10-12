import os, sys, subprocess, datetime
from medleysolver.constants import SAT_RESULT, UNSAT_RESULT, UNKNOWN_RESULT, TIMEOUT_RESULT, ERROR_RESULT, Result, is_solved

import csv 

def run_problem(solver, invocation, problem, timeout):
    instance = problem.split("/", 2)[-1]
    directory = problem[:-len(instance)]
    with open(directory+"/"+solver+".csv") as csvfile:
        results = list(csv.reader(csvfile))
        results = list(filter(lambda s: s[0] == problem, results))
        assert(len(results) == 1)
        output = results[0][4]
        output = output2result(problem, output)
        elapsed = float(results[0][3])

    if elapsed >= timeout:
        output = TIMEOUT_RESULT % timeout
        elapsed = timeout

    result = Result(
        problem  = problem.split("/", 2)[-1],
        result   = output,
        elapsed  = elapsed
    )
    return result

def output2result(problem, output):
    # it's important to check for unsat first, since sat
    # is a substring of unsat
    if 'UNSAT' in output or 'unsat' in output:
        return UNSAT_RESULT
    if 'SAT' in output or 'sat' in output:
        return SAT_RESULT
    if 'UNKNOWN' in output or 'unknown' in output:
        return UNKNOWN_RESULT

    # print(problem, ': Couldn\'t parse output', file=sys.stderr)
    return ERROR_RESULT