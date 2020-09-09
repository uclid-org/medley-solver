medley ./tmp/ nearest.csv -c neighbor
medley ./tmp/ random.csv -c random
medley ./tmp/ neural.csv -c MLP
medley ./tmp/ thompson.csv -c thompson
medley ./tmp/ linucb.csv -c linear
medley ./tmp/ z3.csv -c preset --preset Z3
medley ./tmp/ cvc4.csv -c preset --preset CVC4
medley ./tmp/ yices.csv -c preset --preset YICES
medley ./tmp/ boolector.csv -c preset --preset BOOLECTOR
