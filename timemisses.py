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
        times = eval(row[6])
        solvers = [s for s in eval(row[5])[:len(times)]]
        zipped = zip(solvers, times)

        for (a, b) in zipped:
            if b > 0 and cols[a][r] > b and cols[a][r] < 60:
                print(r, a, cols[a][r], b)
