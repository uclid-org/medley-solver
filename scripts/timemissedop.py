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
benefit = 0
# print("solver, answer, guess, problem")
# Load nearest, zip times with solvers
with open("%s/%s/%s.csv"%(path, dataset, learner)) as csvfile:
    spamreader = list(csv.reader(csvfile))
    for r in range(len(spamreader)):
        row = spamreader[r]
        times = eval(row[6])
        solvers = [s for s in eval(row[5])[:len(times)]]
        zipped = zip(solvers, times)


        for (a, b) in list(zipped)[:1]:
            if b >= 60 and a in cols and row[0] in cols[a] and cols[a][row[0]] >= 60:
                # print(",".join([str(a), str(cols[a][row[0]]), str(b), str(row[0])]))
                # benefit += 60 - b
                benefit += 1

print(benefit)