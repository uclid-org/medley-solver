# MedleySolver

## About
MedleySolver is an algorithm selection tool for SMT queries. After receiving a directory of .smt2 queries as input, it attempts to optimally dispatch its pool of solvers in an optimal way. MedleySolver comes with multiple classification methods, including multiple approaches to the Multi Armed Bandit Problem and a novel nearest neighbor which appears to outperform all other approaches. MedleySolver is highly configurable, but can also be run without any modification to deliver speedup instantly. 

## Installation

1. Install as many SMT solvers as desired. Our recommendations are 
[z3](https://github.com/Z3Prover/z3)
, 
[CVC4](https://cvc4.github.io/), 
[Yices](https://yices.csl.sri.com/), and 
[Boolector](https://boolector.github.io/). MedleySolver requires access to a diverse and competitive set of SMT solvers in order to provide results.

2. Add shell invocations for each solver to the SOLVERS dictionary in medleysolver/constants.py. 

3. Run the following command:
```
    python3 setup.py install
```
4. MedleySolver is ready to run! It can be run with the following line:
```
    // medley [input folder of smt queries] [output csv file]
    medley ~/folder/ results.csv
```
Documentation for usage is available by running:
```
    medley -h
```
