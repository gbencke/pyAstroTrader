import os
import datetime
import multiprocessing

from pyastrotrader.constants import *

NATAL_DATES = {
    'PETR4.SA' : '1953-10-03T19:05:00-03:00', 
    'VALE3.SA' : '1997-05-06T17:47:00-03:00',
    'ITUB4.SA' : '2008-11-04T10:00:00-03:00',
    'BBDC4.SA' : '1943-03-10T10:00:00-03:00',
    'ABEV3.SA' : '1999-07-01T10:00:00-03:00'
}

DATE_MINIMAL_STOCK = {
    'PETR4.SA' : datetime.datetime.strptime('1996-02-01', '%Y-%m-%d')
}

NPARTITIONS = multiprocessing.cpu_count() * 2

SWING_TRADE_DURATION = 5
SWING_EXPECTED_VOLATILITY = 3.5
STAGNATION_THRESHOLD = 5
TOP_THRESHOLD = 2
DAYS_TO_PREDICT = 45

if 'ASSET_TO_CALCULATE' not in os.environ:
    raise ValueError("ASSET_TO_CALCULATE was not set...")
    
ASSET_TO_CALCULATE = os.environ['ASSET_TO_CALCULATE']    
NATAL_DATE = NATAL_DATES[ASSET_TO_CALCULATE]
DEFAULT_PARAMETERS = './config/default_parameters.json'
DEFAULT_CONFIG = './config/default_config.json'

SOURCE_FILE = "./input/{}_Daily".format(ASSET_TO_CALCULATE)

ETA = 0.3
DEPTH = 5
NUM_TREES = 250
MAX_INTERACTIONS = 50
MIN_PRECISION = 0.00001

param = {}
param['booster'] = 'gbtree'
param['objective'] = 'reg:squarederror'
param['eval_metric'] = 'rmse'
param['tree_method'] = 'auto'
param['silent'] = 0
param['subsample'] = 0.5

PLANETS_TO_CALCULATE = [SUN, MOON, VENUS, MERCURY, MARS, JUPITER]
ASPECTS_TO_CALCULATE = [CONJUNCTION, SQUARE, TRINE, OPPOSITION]

DATE_MINIMAL = datetime.datetime.strptime('1998-01-01', '%Y-%m-%d')
