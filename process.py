#!/usr/bin/python3

import csv 
import os
import glob
import sys

TIMEOUT = 60

dataset = sys.argv[1]

extension = 'csv'
os.chdir(dataset)
solvers = sorted(glob.glob('*.{}'.format(extension)))
times = [[] for i in range(len(solvers))]
answers = [[] for i in range(len(solvers))]

for i in range(len(solvers)):
    with open(solvers[i]) as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            r = float(row[3]) if isinstance(row[3], str) else row[3]
            r = r if r < 60 else 60
            times[i].append(r)
            answers[i].append(row[4])

totaltimes = [str(sum(time)) for time in times]
totalcount = [str(sum(map(lambda x: 1 if x == "sat" or x == "unsat" else 0, answer))) for answer in answers]

print(",".join(solvers))
print(",".join(totaltimes))
print(",".join(totalcount))
