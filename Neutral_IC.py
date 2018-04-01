# -*- coding: utf-8 -*-

import os
import pickle
#import numpy as np
import pandas as pd
import statsmodels.api as sm

industry = pd.read_pickle\
    (r'G:\short_period_mf\industry.pkl').drop_duplicates()

return_data = pd.read_pickle\
    (r'G:\short_period_mf\dailyreturn.pickle').rename(columns={'symbol':'code'})

def resid(x, y):
    return sm.OLS(x, y).fit().resid
    
def Neutral_process(alpha_data, saf):
    num_mint = alpha_data.shape[1]
    num_inds = industry.shape[1]
    data = pd.merge(alpha_data, industry, on=['code']).dropna()
    X = data.iloc[:, 1:num_mint]
    y = data.iloc[:, num_mint:num_mint+num_inds]
    X = X.apply(lambda x:resid(x, y))
    X['code'] = alpha_data['code']
#    output = open(r'G:/short_period_mf/netual_process/netual_%s'%saf[-16:],'wb') 
    output = open(r'G:/short_period_mf/netual_day_process/netual_%s'%saf[-16:],'wb')
    pickle.dump(X,output)
    output.close()
    return X

#
#standard_alpha = os.listdir(r'G:/short_period_mf/alpha_min_stand')
standard_alpha = os.listdir(r'G:/short_period_mf/alpha_day_stand')

for saf in standard_alpha:
    alpha_d = pd.read_pickle(r'G:/short_period_mf/alpha_day_stand/%s'%saf)
    Neutral_process(alpha_d,saf)