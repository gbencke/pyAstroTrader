#!/bin/bash

#Create a virtualenv if it doesnt exist
if [ ! -d "./env" ]; then
        virtualenv -p python3 env
        source env/bin/activate
        pip install -r requirements.txt
else
        source env/bin/activate
fi

#Load the virtualenv created

export PYTHONPATH=$PYTHOPATH:$PWD
export SWISSEPH_PATH=$PWD/pyastrotrader/swisseph

#Start the jupyter lab...
cd notebooks
jupyter lab --ip='*' --port=8080 --no-browser
