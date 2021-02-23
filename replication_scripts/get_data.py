import os, subprocess, random, csv, tqdm, sys
from shutil import copy2

BSET = ""
TRAIN_CSV_NAME = ""
RESULTS_CSV_NAME = ""

def clean():
    os.system("rm -rf lib")
    os.system("rm -rf "+BSET+"/train")
    os.system("rm -rf "+BSET+"/test")
    os.mkdir("lib")
    os.mkdir(BSET+"/train")
    os.mkdir(BSET+"/test")


def partition():
    global BSET
    files = os.listdir(BSET)
    files = [f for f in files if f.endswith('.smt2') and 'testcase4.stp.smt2' not in f]
    random.shuffle(files)
    train, test = files[:int(0.4 * len(files))], files[int(0.4 * len(files)):]
    for f in train:
        copy2(BSET+"/"+f, BSET+"/train/"+f)
    for f in test:
        copy2(BSET+"/"+f, BSET+"/test/"+f)
    os.system("cp {}/*.csv {}/test".format(BSET, BSET))
    os.system("cp {}/*.csv {}/train".format(BSET, BSET))
    return train, test

def gen_train_csv(train):
    global BSET
    global TRAIN_CSV_NAME
    csvs = [f for f in os.listdir(BSET) if f.endswith('.csv')]
    ff = open(TRAIN_CSV_NAME, 'w')
    writer = csv.writer(ff)
    writer.writerow(['benchmark', 'solver', 'score'])
    lookup = {}
    for f in csvs:
        fp = open(BSET + f, 'r')
        data = list(csv.reader(fp))
        for row in data:
            fn = os.path.basename(row[0])
            if fn in train:
                writer.writerow([BSET+fn, row[2], row[3] if 'sat' in row[4] else 120])
            else:
                lookup[(row[2], fn)] = row
    return lookup




def machsmt_train():
    global TRAIN_CSV_NAME
    print("machsmt_build -f " + TRAIN_CSV_NAME + " -l lib")
    os.system("machsmt_build -f " + TRAIN_CSV_NAME + " -l lib")
    os.system("machsmt_eval -l lib")


def machsmt(query):
    global BSET
    out = subprocess.check_output(["machsmt", BSET+query, "-l", "lib"])
    solver = out.decode('utf-8').split('\n')[0]
    return solver



def eval(test, lookup):
    global RESULTS_CSV_NAME
    fp = open(RESULTS_CSV_NAME, 'w')
    writer = csv.writer(fp)
    for query in tqdm.tqdm(test):
        solver = machsmt(query)
        if (solver, query) not in lookup:
            writer.writerow([query, [], "error", 120, "error", "error", "error"])
        else:
            l = lookup[(solver, query)]
            writer.writerow([query, [], solver, l[3], l[4], l[5], l[6]])


def main():
    global BSET
    global TRAIN_CSV_NAME
    global RESULTS_CSV_NAME
    if len(sys.argv) != 4:
        raise Exception("Incorrect num args.")
    BSET, TRAIN_CSV_NAME, RESULTS_CSV_NAME = sys.argv[1]+"/", sys.argv[2], sys.argv[3]
    clean()
    train, test = partition()
    lookup = gen_train_csv(train)

    machsmt_train()
    eval(test, lookup)

if __name__ == "__main__":
    # execute only if run as a script
    main()
