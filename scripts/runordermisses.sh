total=0

for seed in 1; do
    for learner in knearest linear MLP thompson exp3a; do
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
        for feature in probes; do
            for reward in binary; do
                val=$(scripts/ordermisses.py ./$1/ ${learner}_${feature}_${reward}_perfect_${seed})
                total=$total+$val
            done 
        done 
    done 
done 

echo \($total\)/5