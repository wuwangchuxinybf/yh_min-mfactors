# -*- coding: utf-8 -*-

import os
import pickle
#import numpy as np
import pandas as pd
import statsmodels.api as sm

Nstyle_factors_files = 'G:/short_period_mf/style_factors/'

def poss_symbol(symbol):
    if len(str(symbol)) == 1:
        return '00000'+str(symbol)
    elif len(str(symbol)) == 2:
        return '0000'+str(symbol)
    elif len(str(symbol)) == 3:
        return '000'+str(symbol)
    elif len(str(symbol)) == 4:
        return '00'+str(symbol)
    elif len(str(symbol)) == 5:
        return '0'+str(symbol)
    else:
        return str(symbol)

def add_exchange(symbol):
    if symbol[:2]=='60':
        return symbol+'.SH'
    else:
        return symbol+'.SZ'

# 第一步 读取行业数据和个股收益率
industry = pd.read_pickle\
    ('G:/short_period_mf/industry.pkl').drop_duplicates()

return_data = pd.read_pickle\
    ('G:/short_period_mf/dailyreturn.pickle').rename(columns={'symbol':'code'})

# 第二步 读取风格因子数据
# 因子数据截止到2017-12-06日
style_filenames = os.listdir(Nstyle_factors_files)
style_filenames.pop(1)  # 不要BP数据
style_list = []
for sfilename in style_filenames:
    style_list.append(sfilename[:-4])
    names = locals()
    names[sfilename[:-4]] = pd.read_csv(Nstyle_factors_files+sfilename)
    names[sfilename[:-4]] = eval(sfilename[:-4])[eval(sfilename[:-4])['date']>='2017-01-01']
    
# 第三步 因子值回归
def resid(x, y):
    return sm.OLS(x, y).fit().resid
    
def Neutral_process(alpha_data, saf):
    alpha_data['code'] = alpha_data['code'].apply(lambda x:add_exchange(poss_symbol(x)))
    num_mint = alpha_data.shape[1]
    num_inds = industry.shape[1]
    data = pd.merge(alpha_data, industry, on=['code']).dropna()
    X = data.iloc[:, 1:num_mint]
    y = data.iloc[:, num_mint:num_mint+num_inds]
    X = X.apply(lambda x:resid(x, y))
    X['code'] = alpha_data['code']
#    output = open('G:/short_period_mf/netual_process/netual_%s'%saf[-16:],'wb') 
    output = open('G:/short_period_mf/netual_day_process/netual_%s'%saf[-16:],'wb')
    pickle.dump(X,output)
    output.close()
    return X

#
#standard_alpha = os.listdir(r'G:/short_period_mf/alpha_min_stand')
standard_alpha = os.listdir('G:/short_period_mf/alpha_day_stand')

for saf in standard_alpha:
    alpha_d = pd.read_pickle('G:/short_period_mf/alpha_day_stand/%s'%saf)
    Neutral_process(alpha_d,saf)
    
    
