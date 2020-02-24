import os
import gc

import pandas as pd
import numpy as np

from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split as ttsplit
from sklearn.metrics import mean_squared_error as mse

import xgboost as xgb
from xgboost import XGBClassifier
from xgboost import plot_importance
from xgboost import plot_tree


from pyastrotrader.constants import *
from pyastrotrader import get_degrees, get_degree
from settings import *

charts = {}
aspects = {}
aspects_transiting = {}

def correct_date(x):
    date_str = str(x['Date'])
    return date_str[0:4] + '-' + date_str[4:6] + '-' + date_str[6:8]    

def change_sign(x,y):
    return  not ((x > 0 and y > 0) or (x < 0 and y < 0))

def get_previous_stock_price(df, x, swing_trade_duration):
    if x['Counter'] > (swing_trade_duration - 1):
        return float(df[df['Counter'] == (x['Counter'] - swing_trade_duration)]['Price'])
    else:
        return 0

def get_future_stock_price(df, x, max, swing_trade_duration):
    if x['Counter'] < (max - swing_trade_duration):
        return float(df[df['Counter'] == (x['Counter'] + swing_trade_duration)]['Price'])
    else:
        return 0    
    
def get_future_stock_max_price(df, x, max, swing_trade_duration):
    if x['Counter'] < (max):
        current_range = df[df['Counter'] <= (x['Counter'] + swing_trade_duration)]
        current_range = current_range[current_range['Counter'] > x['Counter']]
        return current_range['High'].max()
    else:
        return 0        

def get_future_stock_min_price(df, x, max, swing_trade_duration):
    if x['Counter'] < (max):
        current_range = df[df['Counter'] <= (x['Counter'] + swing_trade_duration)]
        current_range = current_range[current_range['Counter'] > x['Counter']]
        return current_range['High'].min()
    else:
        return 0        
    
def calculate_current_trend(x):
    if x['PreviousStartPrice'] > 0.0:
        return ((float(x['Price']) / float(x['PreviousStartPrice'])) - 1) * 100
    else:
        return 0;

def get_previous_stock_date(df, x, swing_trade_duration):
    if x['Counter'] > (swing_trade_duration - 1):
        return float(df[df['Counter'] == (x['Counter'] - swing_trade_duration)]['Date'])
    else:
        return 0

def get_future_stock_date(df, x, max, swing_trade_duration):
    if x['Counter'] < (max - swing_trade_duration):
        return float(df[df['Counter'] == (x['Counter'] + swing_trade_duration)]['Date'])
    else:
        return 0    

def calculate_future_trend(x):
    if x['FutureFinalPrice'] > 0:
        return ((float(x['FutureFinalPrice']) / float(x['Price'])) - 1) * 100
    else:
        return 0;

def calculate_intraday_volatility(df, x, swing_trade_duration):
    current_range = df[df['Counter'] >= (x['Counter'] - (swing_trade_duration * 2))]
    current_range = current_range[current_range['Counter'] < x['Counter']]
    return (((current_range['High'] / current_range['Low']) - 1).sum() / (swing_trade_duration * 2)) * 100

def calculate_swing_strenght(x):
    if float(x['CurrentTrend']) != 0 and float(x['FutureTrend'] != 0):
        return abs(float(x['CurrentTrend']) - float(x['FutureTrend']))
    else:
        return 0

def detect_swing_trade(x, swing_expected_volatility):
    return 1 if change_sign(x['FutureTrend'], x['CurrentTrend']) and \
                x['SwingStrength'] > (x['IntradayVolatility'] * swing_expected_volatility) and \
                abs(x['FutureTrend']) >= abs(x['CurrentTrend']) else 0

def clean_swing_trade(df, x, swing_trade_duration):
    if x['IsSwing'] == 1:
        current_range = df[df['Counter'] <= (x['Counter'] + swing_trade_duration)]
        current_range = current_range[current_range['Counter'] > x['Counter']]
        if current_range['IsSwing'].sum() > 0:
            return 0
        else:
            return 1
    else:
        return 0
    
def detect_price_increase(x, stagnation_threshold):
    return min(stagnation_threshold * TOP_THRESHOLD, (((x['FutureTrendMax'] / x['Open']) - 1)) * 100) \
               if x['FutureTrendMax'] > x['Open'] and x['FutureTrendMax'] > 0 else 0

def clean_price_increase(df, x, swing_trade_duration):
    if x['StockIncreasedPrice'] == 1:
        current_range = df[df['Counter'] >= (x['Counter'] - swing_trade_duration)]
        current_range = current_range[current_range['Counter'] < x['Counter']]
        if current_range['StockIncreasedPrice'].sum() > 0:
            return 0
        else:
            return 1
    else:
        return 0

def detect_price_decrease(x, stagnation_threshold):
    return min(stagnation_threshold * TOP_THRESHOLD, (((x['Open'] / x['FutureTrendMin']) - 1)) * 100) \
               if x['FutureTrendMin'] <= x['Open'] and x['FutureTrendMin'] > 0 else 0

def clean_price_decrease(df, x, swing_trade_duration):
    if x['StockDecreasedPrice'] == 1:
        current_range = df[df['Counter'] >= (x['Counter'] - swing_trade_duration)]
        current_range = current_range[current_range['Counter'] < x['Counter']]
        if current_range['StockDecreasedPrice'].sum() > 0:
            return 0
        else:
            return 1
    else:
        return 0

def detect_price_stagnated(x, stagnation_threshold):
    return 0 if detect_price_increase(x, stagnation_threshold) > stagnation_threshold or \
                detect_price_decrease(x, stagnation_threshold) > stagnation_threshold else 1

def clean_price_stagnated(df, x, swing_trade_duration):
    if x['StockStagnated'] == 1:
        current_range = df[df['Counter'] <= (x['Counter'] + swing_trade_duration)]
        current_range = current_range[current_range['Counter'] > x['Counter']]
        if current_range['StockStagnated'].sum() > 0:
            return 0
        else:
            return 1
    else:
        return 0
    
def is_aspected(row, first_planet, second_planet, aspect):
    c_transits = aspects[row['CorrectedDate']]
    found_params = [x for x in c_transits if (x['c_planet'] == first_planet and x['n_planet'] == second_planet and x['c_aspect'] == aspect) or \
                                           (x['n_planet'] == first_planet and x['c_planet'] == second_planet and x['c_aspect'] == aspect) ]
    return 1 if len(found_params) > 0 else 0

def is_aspected_transiting(row, first_planet, second_planet, aspect):
    c_transits = aspects_transiting[row['CorrectedDate']]
    found_params = [x for x in c_transits if (x['c_planet'] == first_planet and x['n_planet'] == second_planet and x['c_aspect'] == aspect) or \
                                           (x['n_planet'] == first_planet and x['c_planet'] == second_planet and x['c_aspect'] == aspect) ]
    return 1 if len(found_params) > 0 else 0


def is_retrograde(row, planet):
    if planet in [SUN,MOON]:
        return 0
    c_chart = charts[row['CorrectedDate']]
    return 1 if c_chart['planets']['planets_retrograde'][planet] else 0   


def get_degrees_for_planets(row, first_planet, second_planet):
    c_chart = charts[row['CorrectedDate']]
    return abs(get_degrees(c_chart, first_planet, second_planet))

def get_degree_for_planet(row, planet):
    c_chart = charts[row['CorrectedDate']]
    return get_degree(c_chart, planet)

def calculate_price_change(df, row):
    if row['Counter'] > 1:
        if ((float(row['Price']) / float(df[df['Counter'] == row['Counter'] -1]['Price'])) - 1) * 100 > 1:
            return 1
        else:
            if ((float(row['Price']) / float(df[df['Counter'] == row['Counter'] -1]['Price'])) - 1) * 100 < -1:
                return -1
    return 0

def create_booster_swing_trade(eta,depth,num_trees, train_x, train_y, test_x, test_y, columns, trained_model):
    param['max_depth'] = depth
    param['eta'] = eta
    num_round = num_trees
    dtrain = xgb.DMatrix(train_x, train_y, feature_names = columns)
    dtest = xgb.DMatrix(test_x, test_y, feature_names = columns)
    train_labels = dtrain.get_label()
    gpu_res = {}
    booster = xgb.train(param, dtrain, num_round, evals_result=gpu_res, evals = [], xgb_model = trained_model)    
    return booster

def get_best_booster(target_variable, max_interactions, df, astro_columns):
    booster = None
    best_score = 1
    best_booster = None
    for current_run in range(max_interactions):
        X = df[astro_columns].values
        Y = df[target_variable].values
        total_test = xgb.DMatrix(X, feature_names = astro_columns)
        X_train_1, X_train_2, y_train_1, y_train_2 = ttsplit(X, Y, 
                                                             test_size=0.3, 
                                                             random_state=None,
                                                             shuffle=True)
        booster = create_booster_swing_trade(
            ETA, DEPTH, NUM_TREES, 
            X_train_1, y_train_1, 
            X_train_2, y_train_2, 
            astro_columns, booster)
        current_score = mse(booster.predict(total_test), Y)
        if current_score < best_score:
            best_score = current_score
            best_booster = booster
        gc.collect()
        print("{} - {} of {}, {}".format(target_variable, current_run, max_interactions, best_score))
        if best_score < MIN_PRECISION:
            break
    return best_booster, best_score

def predict_score(row, booster, df, astro_columns):
    matrix_to_predict = row[astro_columns].values
    matrix_to_predict = matrix_to_predict.reshape((1,-1))
    row_features = xgb.DMatrix(matrix_to_predict, feature_names = astro_columns)
    predicted = booster.predict(row_features)[0]
    if predicted > 1:
        predicted = 1
    if predicted < -1:
        predicted = -1
    return predicted    