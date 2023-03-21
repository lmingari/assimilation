#!/bin/bash

FILES="00?/validation_metrics.csv"
OUTFILE="validation_metrics.csv"

for f in $FILES
do
    echo "Reading file $f"
    if [ -z "$header" ]; then
        header=`head -n 1 $f`
        echo $header > $OUTFILE
    fi
    tail -n +2 $f >> $OUTFILE
done
