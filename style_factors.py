# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 20:56:15 2018

@author: wuwangchuxin
"""

import pandas as pd

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
    
df = pd.read_csv(r'C:\Users\wuwangchuxin\Desktop\yinhua_min\data\Barra\Beta_CNE5_T+1.csv')
col = list(df.columns)
col[1:] = map(poss_symbol,col[1:])
col[0] = 'date' 
df.columns = col

















































































