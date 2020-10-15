for seed in 0; do #1; do
    for learner in random; do #thompson knearest MLP linear exp3a; do
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
                # medley ./$1/ ./$1/${learner}_${feature}_${reward}_const_${seed}.csv   --classifier $learnconfig --seed $seed --feature_setting $feature --reward $reward --timeout_manager const --set_const 60
                medley ./$1/ ./$1/${learner}_${feature}_${reward}_perfect_${seed}.csv    --classifier $learnconfig --seed $seed --feature_setting $feature --reward $reward --timeout_manager perfect
                # medley ./$1/ ./$1/${learner}_${feature}_${reward}_5_nearest_${seed}.csv --classifier $learnconfig --seed $seed --feature_setting $feature --reward $reward --timeout_manager nearest --time_k 20
            done 
        done 
    done 
done 