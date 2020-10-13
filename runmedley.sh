medley ./$1/ ./$1/thompson.csv -c thompson -k full -e True
medley ./$1/ ./$1/nearest.csv -c neighbor -k full -e True
medley ./$1/ ./$1/random.csv -c random -e True
medley ./$1/ ./$1/MLP.csv -c MLP -e True
medley ./$1/ ./$1/linear.csv -c linear -e True
medley ./$1/ ./$1/exp3.csv -c exp3 -e True

medley ./$1/ ./$1/thompson_last.csv -c thompson -k full -e False
medley ./$1/ ./$1/nearest_last.csv -c neighbor -k full -e False
medley ./$1/ ./$1/random_last.csv -c random -e False
medley ./$1/ ./$1/MLP_last.csv -c MLP -e False
medley ./$1/ ./$1/linear_last.csv -c linear -e False
medley ./$1/ ./$1/exp3_last.csv -c exp3 -e False


# medley ./$1/ ./$1/thompsonsingle.csv -c thompson -k single
# medley ./$1/ ./$1/thompsongreedy.csv -c thompson -k greedy
# medley ./$1/ ./$1/nearestsingle.csv -c neighbor -k single
# medley ./$1/ ./$1/nearestgreedy.csv -c neighbor -k greedy