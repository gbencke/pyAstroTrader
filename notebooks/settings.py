import os

from pyastrotrader.constants import *

NATAL_DATES = {
    'PETR4' : '1953-10-03T19:05:00-03:00'
}

SWING_TRADE_DURATION = 5
SWING_EXPECTED_VOLATILITY = 3.5
STAGNATION_THRESHOLD = 5

if 'ASSET_TO_CALCULATE' not in os.environ:
    raise ValueError("ASSET_TO_CALCULATE was not set...")
    
ASSET_TO_CALCULATE = os.environ['ASSET_TO_CALCULATE']    
NATAL_DATE = NATAL_DATES[ASSET_TO_CALCULATE]
DEFAULT_PARAMETERS = './config/default_parameters.json'
DEFAULT_CONFIG = './config/default_config.json'

SOURCE_FILE = "./input/{}_Daily".format(ASSET_TO_CALCULATE)

ETA = 0.3
DEPTH = 5
NUM_TREES = 100
MAX_INTERACTIONS = 100

param = {}
param['booster'] = 'gbtree'
param['objective'] = 'binary:logistic'
param['eval_metric'] = 'auc'
param['tree_method'] = 'auto'
param['silent'] = 0
param['subsample'] = 0.5

PLANETS_TO_CALCULATE = [SUN,MOON,SATURN, JUPITER, VENUS, MARS]
ASPECTS_TO_CALCULATE = [CONJUNCTION, SQUARE, TRINE, OPPOSITION]
