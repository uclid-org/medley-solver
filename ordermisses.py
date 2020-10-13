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
    cols[r[:-len(".csv")]] = {}

for r in result:
    solver = r[:-len(".csv")]
    with open(r) as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            r = float(row[3]) if isinstance(row[3], str) else row[3]
            r = r if r < 60 else 60
            r = r if row[4] != "error" and "timeout" not in row[4] else 60
            cols[solver][row[0]] = r

print("choice, answer, problem")
# Load nearest, zip times with solvers
with open("%s/%s/%s.csv"%(path, dataset, learner)) as csvfile:
    spamreader = list(csv.reader(csvfile))
    for r in range(len(spamreader)):
        row = spamreader[r]
        runtimes = eval(row[6])
        solvers = eval(row[5])[:len(runtimes)]

        solvers = [solvers[i] for i in range(len(solvers)) if runtimes[i] > 0 and solvers[i] in cols and row[0] in cols[solvers[i]]]

        times = [cols[a][row[0]] for a in solvers]

        index_min = min(range(len(times)), key=times.__getitem__)

        if index_min != 0:
            print(",".join([str(solvers[0]), str(solvers[index_min], str(row[0]))]))
