medley ./$1/ ./$1/thompson.csv -c thompson
medley ./$1/ ./$1/nearest.csv -c neighbor
medley ./$1/ ./$1/knearest.csv -c knearest --k 10
medley ./$1/ ./$1/random.csv -c random 
medley ./$1/ ./$1/MLP.csv -c MLP 
medley ./$1/ ./$1/linear.csv -c linear 
medley ./$1/ ./$1/exp3.csv -c exp3 

medley ./$1/ ./$1/thompson_only.csv -c thompson --timeout_manager const --set_const 60
medley ./$1/ ./$1/nearest_only.csv -c neighbor --timeout_manager const --set_const 60
medley ./$1/ ./$1/knearest_only.csv -c knearest --k 10 --timeout_manager const --set_const 60
medley ./$1/ ./$1/random_only.csv -c random --timeout_manager const --set_const 60
medley ./$1/ ./$1/MLP_only.csv -c MLP --timeout_manager const --set_const 60
medley ./$1/ ./$1/linear_only.csv -c linear --timeout_manager const --set_const 60
medley ./$1/ ./$1/exp3_only.csv -c exp3 --timeout_manager const --set_const 60

medley ./$1/ ./$1/timenearest.csv -c knearest --k 10 --timeout_manager nearest --time_k 20