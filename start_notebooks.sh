#!/bin/bash

#Create a virtualenv if it doesnt exist
if [ ! -d "./env" ]; then
        virtualenv -p python3 env
fi

#Load the virtualenv created
source env/bin/activate

#Install the required python modules
pip install -r requirements.txt

#Start the jupyter lab...
cd notebooks
jupyter lab --ip='*' --port=8080 --no-browser
