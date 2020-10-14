for learner in thompson neighbor knearest random MLP linear exp3a exp3b exp3c; do
    sh ./runlearner.sh tmp/BV $learner
    sh ./runlearner.sh tmp/QF_ABV $learner
    sh ./runlearner.sh tmp/QF_AUFBV $learner
done