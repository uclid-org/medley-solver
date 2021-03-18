from inspect import getmembers, isfunction
from medleysolver.constants import keyword_list
import time
import z3
import csv
import json
import os

kw2indx = dict((keyword_list[i],i) for i in range(len(keyword_list)))
cached_counts = {}
cached_checksats = {}

PROBES = [
    'size',
    'num-exprs',
    'num-consts',
    'arith-avg-deg',
    'arith-max-bw',
    'arith-max-bw',
    'arith-avg-bw',
    'depth',
    'num-bool-consts',
    'num-arith-consts',
    'num-bv-consts'
]

COUNT_TIMEOUT = 1.0

def get_syntactic_count_features(file_path):
    tic = time.time()
    features = [0.0] * len(keyword_list)
    n = 0
    v = -1.0
    with open(file_path,'rb') as file:
        for line in file:
            line = line.decode()
            line = line.replace('(', ' ( ')
            line = line.replace(')', ' ) ')
            if line.find(';') != -1:
                line = line[:line.find(';')]
            line = line.split()
            for t in line:
                if t in kw2indx:
                    features[kw2indx[t]] += 1.0
                n+=1
            if time.time() - tic > COUNT_TIMEOUT:
                v = 1.0
                break
        features.append(n)      ##Total Counts
        features.append(v)      ##Timeout?
    return features

cache = {}
def get_features(file_path, feature_setting, features2use, logic="",track=""):
    if not "curr" in cache:
        cache["curr"] = list(csv.reader(open(feature_setting, 'r')))
    all_points = cache["curr"]
    lookup = [f for f in all_points if os.path.basename(file_path) == os.path.basename(f[0])]
    if len(lookup) != 1:
        raise Exception("Error in finding features for", file_path)
    row = lookup[0]
    features = [float(row[i+1]) for i in json.loads(features2use)]
    return features

def get_check_sat(file_path):
    if file_path in cached_checksats:
        return cached_checksats[file_path]
    ret = 0
    with open(file_path,'r') as file:
        for line in file:
            if line.find(';') != -1:
                line = line[:line.find(';')]
            ret += line.count('check-sat')
    cached_checksats[file_path] = ret
    return ret
