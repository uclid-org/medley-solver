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

to_keep = []
with open("%s/%s/%s.csv"%(path, dataset, learner)) as csvfile:
    spamreader = list(csv.reader(csvfile))
    for r in range(len(spamreader)):
        row = spamreader[r]
        name = row[0]
        to_keep.append(name)


for r in result:
    solver = r[:-len(".csv")]
    out = r.split("/")[-1]
    out = "%s/%s500/%s"%(path, dataset, out)
    # Open both files
    with open(r) as f_in, open(out, 'w') as f_out:
        spamreader = list(csv.reader(f_in))
        spamwriter = csv.writer(f_out)
        for line in spamreader:
            name = line[0]
            if name in to_keep:
                spamwriter.writerow(line)