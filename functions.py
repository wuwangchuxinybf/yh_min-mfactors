# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 20:20:33 2018

@author: wuwangchuxin
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm

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
    
def poss_date(date):
    if len(date) == 10:
        return date[:4]+'-'+date[5:7]+'-'+date[8:]
    elif len(date) == 8:
        return date[:4]+'-0'+date[5]+'-0'+date[-1]
    elif date[-2] == r'/':
        return date[:4]+'-'+date[5:7]+'-0'+date[-1]
    else:
        return date[:4]+'-0'+date[5]+'-'+date[-2:]

def add_exchange(symbol):
    if symbol[:2]=='60':
        return symbol+'.SH'
    else:
        return symbol+'.SZ'

def alpha_filename(num):
    if np.log10(num)<1:
        return '00'+str(num)
    elif np.log10(num)<2:
        return '0'+str(num)
    else:
        return str(num)

def stand_fac(data_b):
    x_mean = data_b.mean()   #每一日所有股票的 默认 axis = 0
    x_std = data_b.std()    #每一日所有股票的     
    for j in range(len(data_b.columns)): 
        for i in range(len(data_b)):
            if not np.isnan(data_b.iloc[i,j]):
                if (data_b.iloc[i,j]-x_mean[j])/x_std[j] > 3:
                    data_b.iloc[i,j] = 3*x_std[j]+x_mean[j]
                elif (data_b.iloc[i,j]-x_mean[j])/x_std[j] < -3:
                    data_b.iloc[i,j] = -3*x_std[j]+x_mean[j] #(x_mean[i]-3*x_std[i])   
    x_mean2 = np.array(data_b.mean())
    x_std2 = np.array(data_b.std())
    data_c = pd.DataFrame(index = data_b.index,columns = data_b.columns)
    for k in range(len(data_b.columns)):
        data_c.iloc[:,k] = data_b.iloc[:,k].fillna(x_mean2[k])
    data_d = np.array(data_c)        
    data_d = (data_d-x_mean2)/x_std2
    return data_d   
    
def resid(x, y):
    return sm.OLS(x, y).fit().resid

def beta_value(x, y):
    return sm.OLS(x, y).fit().params

def possess_alpha(alpha_data, saf):
    alpha_data['code'] = alpha_data['code'].apply(lambda x:add_exchange(poss_symbol(x)))
    if saf == 'standard_alpha_149.csv':
        mid_columns = ['code'] + [x for x in list(map(poss_date,alpha_data.columns[1:])) \
                      if x >='2017-01-01'and x<='2017-12-06']
        alpha_data.columns = ['code'] + [x for x in list(map(poss_date,alpha_data.columns[1:]))]
    else:
        mid_columns = ['code'] + [x for x in list(alpha_data.columns)[1:] \
                      if x >='2017-01-01'and x<='2017-12-06']    
    alpha_data = alpha_data.loc[:,mid_columns]
    alpha_data.index = alpha_data['code']
    alpha_data.drop(['code'],axis = 1,inplace = True)
    alpha_data = alpha_data.T
    alpha_data.reset_index(inplace = True)
    alpha_data.rename(columns={'index':'date'},inplace = True)
    return alpha_data
    
    
    
    















