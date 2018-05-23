# -*- coding: utf-8 -*-
"""
Created on Thu May 10 21:35:15 2018

@author: wuwangchuxin
"""

import os
os.chdir('D:/yh_min-mfactors')
from address_data import *
import feather as ft
import pandas as pd
import pickle

marketData = pd.read_feather(add_day_file + 'marketData.feather')
test = marketData.head()
tmp = marketData[['date','symbol','name','publicDate','idxWeight_hs300']]

code_HS300 = pd.read_excel(add_gene_file + 'data_mkt.xlsx',sheetname='HS300')
stockList = list(code_HS300['code'][:])
stockList = list(map(lambda x : x[:6],stockList))

tmp = tmp[tmp['symbol'].isin(stockList)]
tmp2 = tmp[tmp['date']>='2010-01-01']
tmp2.to_csv(r'G:\short_period_mf\weight_hs300.csv')
