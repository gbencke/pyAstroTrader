#!/bin/bash

if [ -z '$ASSET_TO_CALCULATE' ]
then
        echo 'Please set the ASSET_TO_CALCULATE environment variable'
        exit -1
fi

if [ -z '$ALPHAVANTAGE_KEY' ]
then
        echo 'Please set the ALPHAVANTAGE_KEY environment variable'
        exit -1
fi

if [ -z '$MODEL' ]
then
        echo 'Please set the MODEL environment variable'
        exit -1
fi

#Create a virtualenv if it doesnt exist
if [ ! -d "./env" ]; then
        virtualenv -p python3 env
        source env/bin/activate
        pip install -r requirements.txt
else
        source env/bin/activate
fi

#Load the virtualenv created

export PYTHONPATH=$PYTHOPATH:$PWD:$PWD/notebooks
export SWISSEPH_PATH=$PWD/pyastrotrader/swisseph

date > start.txt

rm -rf ./notebooks/output/*
cd notebooks

count=0
MAX_INTERACTIONS=50


jupyter nbconvert --ExecutePreprocessor.timeout=-1 --execute DownloadData.ipynb

while [ $count -lt $MAX_INTERACTIONS ]
do
        echo "Running:$count"
        if [ $MODEL == "PRICE_CHANGE" ]
        then
                jupyter nbconvert --ExecutePreprocessor.timeout=-1 --execute CreateModel.price.change.ipynb
                jupyter nbconvert --ExecutePreprocessor.timeout=-1 --execute Predict.price.change.ipynb
        fi
        if [ $MODEL == "SWING_TRADE" ]
        then
                jupyter nbconvert --ExecutePreprocessor.timeout=-1 --execute CreateModel.swing.trade.ipynb
                jupyter nbconvert --ExecutePreprocessor.timeout=-1 --execute Predict.swing.trade.ipynb
        fi
        count=`expr $count + 1`
done

cd ..

source ./clean_notebooks.sh

date > end.txt
