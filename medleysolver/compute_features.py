from inspect import getmembers, isfunction
from medleysolver.constants import keyword_list
import time
import z3

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
def get_features(file_path,logic="",track=""):
    if file_path not in cache:
        cache[file_path] = {}
    if logic not in cache[file_path]:
        cache[file_path][logic] = {}
    if track not in cache[file_path][logic]:
        cache[file_path][logic][track] = {}

    features = get_syntactic_count_features(file_path)
    g = z3.Goal()
    g.add(z3.parse_smt2_file(file_path))
    results = [z3.Probe(x)(g) for x in PROBES]
    features = features + results

    cache[file_path][logic][track] = features
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
