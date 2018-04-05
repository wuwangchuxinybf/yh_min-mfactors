# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 20:56:15 2018

@author: wuwangchuxin
"""

import pandas as pd
import os

style_factors_files = 'G:/short_period_mf/Barra/'

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
    
filenames = os.listdir(style_factors_files)
for filename in filenames:
    df = pd.read_csv(style_factors_files+filename)
    col = list(df.columns)
    col[1:] = map(poss_symbol,col[1:])
    col[0] = 'date' 
    df.columns = col
    mid_name = filename[:filename.index('_')]
    names = locals()
    names[mid_name] = df
    df.to_csv('G:/short_period_mf/style_factors/%s.csv'%mid_name)

# Beta Momentum Size Earnings_Yield Volatilty Growth、Value、Leverage、Liquidity
#                    EarnYield       ResVol           NLSize



































































