total=0

for seed in 0; do #1; do
    for learner in thompson knearest MLP linear exp3a; do
        if [ $learner = exp3a ]
        then
            learnconfig="exp3 --gamma 0.07"
        elif [ $learner = exp3b ]
        then
            learnconfig="exp3 --gamma 0.1"
        elif [ $learner = exp3c ]
        then
            learnconfig="exp3 --gamma 0.25"
        else 
            learnconfig=$learner
        fi
        for feature in both; do #probes bow; do
            for reward in bump; do # binary exp; do
                val=$(./timemisses.py ./$1/ ${learner}_${feature}_${reward}_${2}_${seed})
                total=$total+$val
            done 
        done 
    done 
done 

echo \($total\)/5