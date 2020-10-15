#!/usr/bin/python3

import csv 
import os
import glob
import sys

path = os.getcwd()

dataset = sys.argv[1]
extension = 'csv'
os.chdir(dataset)
result = glob.glob('*.{}'.format(extension))

result = [r for r in result if "_" not in r]

cols = {}
for r in result:
    cols[r[:-len(".csv")]] = {}

solvers = []

for r in result:
    solver = r[:-len(".csv")]
    solvers.append(solver)
    with open(r) as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            r = float(row[3]) if isinstance(row[3], str) else row[3]
            r = r if r < 60 else 60
            r = r if row[4] != "error" and "timeout" not in row[4] else 60
            cols[solver][row[0]] = r

vbtime = 0
vbsolved = 0
spread = {}

for s in solvers:
    spread[s] = 0

for q in cols[solvers[0]]:
    best_time = 60
    best_solver = ""

    for s in solvers:
        if cols[s][q] < best_time:
            best_time = cols[s][q]
            best_solver = s

    if best_solver != "":
        spread[best_solver] += 1
        vbsolved += 1

    vbtime += best_time

print(vbtime, vbsolved)

for s in spread:
    print(s, spread[s])