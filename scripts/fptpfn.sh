for category in BV QF_ABV Sage2 uclid combined; do
    echo $category
    sh scripts/runtimecost.sh data/$category $1
    sh scripts/runtimebenfit.sh data/$category $1
    sh scripts/runtimemissedop.sh data/$category $1
done