for seed in 0 1; do
    for learner in thompson neighbor knearest random MLP linear exp3a exp3b exp3c exp3d; do
        if [ $learner == exp3a ]
        then
            learnconfig="exp3 --gamma 0.07"
        elif [ $learner == exp3b ]
        then
            learnconfig="exp3 --gamma 0.1"
        elif [ $learner == exp3c ]
        then
            learnconfig="exp3 --gamma 0.25"
        elif [ $learner == exp3c ]
        then
            learnconfig="exp3 --gamma 0.5"
        else 
            learnconfig=$learner
        fi
        for feature in both probes bow; do
            for reward in binary bump exp; do
                medley ./$1/ ./$1/${learner}_${feature}_${reward}_const_${seed}.csv   --classifier $learnconfig --seed $seed --feature_setting $feature --reward $reward --timeout_manager const --set_const 60
                medley ./$1/ ./$1/${learner}_${feature}_${reward}_expo_${seed}.csv    --classifier $learnconfig --seed $seed --feature_setting $feature --reward $reward --timeout_manager expo
                medley ./$1/ ./$1/${learner}_${feature}_${reward}_nearest_${seed}.csv --classifier $learnconfig --seed $seed --feature_setting $feature --reward $reward --timeout_manager nearest --time_k 20
            done 
        done 
    done 
done 