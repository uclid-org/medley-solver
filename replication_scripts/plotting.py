import csv, os, numpy as np, matplotlib.pyplot as plt, random

from scipy.stats import describe


def get_index(a, i):
    return [float(b[i]) if 'sat' in b[4] else float(120) for b in a ]

def race(solver):
    return np.cumsum(get_index(solver, 3))

def process(l, reference):
    ret = []
    for t in reference:
        flag = False
        for i in l:
            if os.path.basename(i[0]) == os.path.basename(t[0]):
                flag = True
                ret.append(i)
                break
        if not flag:
            ret.append([t[0], t[1], '', '60', 'error', '', ''])
    return ret

def training(logic):
    with open(logic+"_train.csv", newline='') as f:
        reader = csv.reader(f)
        a = list(reader)
        a = [float(b[2]) for b in a if b[2] != "score"]
        return sum(a)
    
def relu(x):
    return x * (x > 0)

def var_calc(logic, solver, sneak):
    a = get_index(sneak, 3)
    b1, b2, b3, b4, b5 = (relu(np.random.normal(a, 15)) for _ in range(5))
    random.shuffle(b1)
    random.shuffle(b2)
    random.shuffle(b3)
    random.shuffle(b4)
    random.shuffle(b5)
    plt.plot(np.cumsum(b1))
    plt.plot(np.cumsum(b2))
    plt.plot(np.cumsum(b3))
    plt.plot(np.cumsum(b4))
    plt.plot(np.cumsum(b5))
    return([np.cumsum(b)[-1] for b in [b1, b2, b3, b4, b5]])
    
    
def run_all(logic, currdir, suf=''):
    with open("final_csvs/results/"+logic+"_medley.csv", newline='') as f:
        reader = csv.reader(f)
        med = list(reader)

    with open("final_csvs/results/"+logic+"_machsmt.csv", newline='') as f:
        reader = csv.reader(f)
        mach = list(reader)
        
    with open(currdir+'/Z3{}.csv'.format(suf), newline='') as f:
        reader = csv.reader(f)
        z3 = list(reader)

    with open(currdir+'/YICES{}.csv'.format(suf), newline='') as f:
        reader = csv.reader(f)
        yices = list(reader)

    with open(currdir+'/mathsat{}.csv'.format(suf), newline='') as f:
        reader = csv.reader(f)
        mathsat = list(reader)

    with open(currdir+'/cvc4{}.csv'.format(suf), newline='') as f:
        reader = csv.reader(f)
        cvc4 = list(reader)

    with open(currdir+'/bitwuzla{}.csv'.format(suf), newline='') as f:
        reader = csv.reader(f)
        bitwuzla = list(reader)

    with open(currdir+'/boolector{}.csv'.format(suf), newline='') as f:
        reader = csv.reader(f)
        boolector = list(reader)
    
    s = zip(
        process(z3, mach),
        process(yices, mach),
        process(cvc4, mach),
        process(boolector, mach),
        process(mathsat, mach),
        process(bitwuzla, mach))
    
    vbest = [min(member, key=lambda x: float(x[3]) if 'sat' in x[4] else 120) for member in s]

    vbest_choices = [v[2] for v in process(vbest, mach)]
    msmt_choices = [v[2] for v in process(mach, mach)]
    med_choices = [v[2] for v in process(med, mach)]
    print("Number of differences between machsmt & optimal: ", sum([0 if s[0] == s[1] else 1 for s in zip(vbest_choices, msmt_choices)]))
    print("Number of differences between medley & optimal: ", sum([0 if s[0] == s[1] else 1 for s in zip(vbest_choices, med_choices)]))
    
    plt.plot(race(process(med, mach)), label="med")
    plt.plot(race(process(mach, mach)), label="mach")
    plt.plot(race(process(z3, mach)), label="z3")
    plt.plot(race(process(cvc4, mach)), label="cvc4")
    plt.plot(race(process(boolector, mach)), label="boolector")
    plt.plot(race(process(yices, mach)), label="yices")
    plt.plot(race(process(mathsat, mach)), label="mathsat")
    plt.plot(race(process(bitwuzla, mach)), label="bitwuzla")
    plt.plot(race(process(vbest, mach)), label='vbest')
    plt.legend()
    
    assert len(race(process(med, mach))) == len(race(process(mach, mach)))
    assert len(race(process(med, mach))) == len(race(process(vbest, mach)))
    
    print("diff between med/mach", race(process(med, mach))[-1], race(process(mach, mach))[-1], race(process(vbest, mach))[-1])
    print("Medley solved: ", len([i[4] for i in process(med, mach) if 'sat' in i[4]]))
    print("Machsmt solved: ", len([i[4] for i in process(mach, mach) if 'sat' in i[4]]))
    print("Best possible solved: ", len([i[4] for i in process(vbest, mach) if 'sat' in i[4]]))

    return process(med,mach), process(mach,mach), process(vbest,mach)


def var_plotter(var_files, solver_files):
    suf=''
    with open(var_files+'/0.csv', newline='') as f:
        reader = csv.reader(f)
        ref = list(reader)
        
    with open(solver_files+'/Z3{}.csv'.format(suf), newline='') as f:
        reader = csv.reader(f)
        z3 = process(list(reader), ref)

    with open(solver_files+'/YICES{}.csv'.format(suf), newline='') as f:
        reader = csv.reader(f)
        yices = process(list(reader), ref)

    with open(solver_files+'/mathsat{}.csv'.format(suf), newline='') as f:
        reader = csv.reader(f)
        mathsat = process(list(reader), ref)

    with open(solver_files+'/cvc4{}.csv'.format(suf), newline='') as f:
        reader = csv.reader(f)
        cvc4 = process(list(reader), ref)

    with open(solver_files+'/bitwuzla{}.csv'.format(suf), newline='') as f:
        reader = csv.reader(f)
        bitwuzla = process(list(reader), ref)

    with open(solver_files+'/boolector{}.csv'.format(suf), newline='') as f:
        reader = csv.reader(f)
        boolector = process(list(reader), ref)
        
    s = zip(
        z3, yices, cvc4, mathsat, bitwuzla, boolector)
    
    vbest = [min(member, key=lambda x: float(x[3]) if 'sat' in x[4] else 120) for member in s]
    best_solver = min([z3, yices, cvc4, boolector, mathsat, bitwuzla], key=lambda x: race(x)[-1])
    print("Best Solver: ", best_solver[0][2])
    plt.plot(race(process(best_solver, ref)), label="Best Solver")
    plt.plot(race(process(vbest, ref)), label='Virtual best')
    for filename in os.listdir(var_files):
        with open(var_files+"/"+filename, 'r', newline='') as f:
            next_one = list(csv.reader(f))
        plt.plot(race(next_one), alpha=0.3)
    plt.legend()