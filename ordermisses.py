#!/usr/bin/python3

import csv 
import os
import glob
import sys

path = os.getcwd()

dataset = sys.argv[1]
learner = sys.argv[2]
extension = 'csv'
os.chdir(dataset)
result = glob.glob('*.{}'.format(extension))

cols = {}
for r in result:
    cols[r[:-len(".csv")]] = [] 

for r in result:
    solver = r[:-len(".csv")]
    with open(r) as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            r = float(row[3]) if isinstance(row[3], str) else row[3]
            r = r if r < 60 else 60
            cols[solver].append(r)

# Load nearest, zip times with solvers
with open("%s/%s/%s.csv"%(path, dataset, learner)) as csvfile:
    spamreader = list(csv.reader(csvfile))
    for r in range(len(spamreader)):
        row = spamreader[r]
        runtimes = eval(row[6])
        solvers = eval(row[5])[:len(runtimes)]

        solvers = [solvers[i] for i in range(len(solvers)) if runtimes[i] > 0]

        times = [cols[a][r] for a in solvers]

        index_min = min(range(len(times)), key=times.__getitem__)

        if index_min != 0:
            print(r, solvers[0], solvers[index_min])
