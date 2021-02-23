import os, random, sys

def main():
    if len(sys.argv) != 5:
        raise Exception("wrong num args")

    _, target, seed, trials, out_loc = sys.argv
    random.seed(int(seed))
    for i in range(int(trials)):
        new_seed = random.randint(0, 100000)
        os.system("medley {} {} --seed {}".format(target, out_loc+"/"+str(i)+".csv", str(new_seed)))

if __name__ == "__main__":
    # execute only if run as a script
    main()