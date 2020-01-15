#!/bin/bash

for i in $(cat ./assets_to_calculate.txt)
do
        export ASSET_TO_CALCULATE=$i
        ./run_notebooks.sh
done

