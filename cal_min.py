# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 21:49:28 2018

@author: wuwangchuxin
"""

import os
os.chdir('D:/yh_min-mfactors')
from alphaFuncs_min import *
import pandas as pd
import feather as ft

minute_file_path = 'G:/1m_data/1/'
timeSerialFile='G:/short_period_mf/trade.date'

################ 因子计算结果没有 '600485.SH'（停牌）

# 先验证分钟行情数据的时间范围,分钟和日范围
files = os.listdir(minute_file_path)
res = []
for filename in files:
    df = ft.read_dataframe(minute_file_path+filename, nthreads=100)
    ls = list(df['date'])
    res = list(set(res+ls))  #验证结果,每个股票的时间都是完整的，468480条分钟数据
datetimel = sorted(res)[408000:] #从2017年开始，60480条分钟线数据，每个股票的时间也是完整的   
datel = list(set(map(lambda x : x[:10],datetimel))) # 日数据252条，20170103-20180115


# 沪深300指数成分股
code_HS300 = pd.read_excel('G:/short_period_mf/data_mkt.xlsx',\
              sheetname='HS300')
stockList = list(code_HS300['code'][:])
# 分钟线：从2017-01-03 09:31:00 至 2018-01-15 15:00:00
dateList = open('G:/short_period_mf/trade.date').read().split('\n')
alpha_all(stockList, dateList, savepath='G:/short_period_mf/alpha_min/')




