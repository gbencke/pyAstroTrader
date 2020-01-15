#!/bin/bash

source env/bin/activate

for i in notebooks/*.ipynb
do
    echo "Cleaning:$i"
    jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace $i
done

