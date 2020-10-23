import os, sys, subprocess, datetime
from medleysolver.constants import SAT_RESULT, UNSAT_RESULT, UNKNOWN_RESULT, TIMEOUT_RESULT, ERROR_RESULT, Result, is_solved

import csv 

def run_problem(solver, invocation, problem, timeout):
    # pass the problem to the command
    command = "%s %s" %(invocation, problem)
    # get start time
    start = datetime.datetime.now().timestamp()
    # run command
    process = subprocess.Popen(
        command,
        shell      = True,
        stdout     = subprocess.PIPE,
        stderr     = subprocess.PIPE,
        preexec_fn = os.setsid
    )
    # wait for it to complete
    try:
        process.wait(timeout=timeout)
    # if it times out ...
    except subprocess.TimeoutExpired:
        # kill it
        # print('TIMED OUT:', repr(command), '... killing', process.pid, file=sys.stderr)
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGINT)
        except:
            pass
        # set timeout result
        elapsed = timeout
        output  = TIMEOUT_RESULT % timeout
    # if it completes in time ...
    else:
        # measure run time
        end     = datetime.datetime.now().timestamp()
        elapsed = end - start
        # get result
        stdout = process.stdout.read().decode("utf-8", "ignore")
        stderr = process.stderr.read().decode("utf-8", "ignore")
        output = output2result(problem, stdout + stderr)
    # make result
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