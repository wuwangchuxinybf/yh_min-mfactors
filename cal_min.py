# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 21:49:28 2018

@author: wuwangchuxin
"""

import os
os.chdir('D:/yh_min-mfactors')
from alphaFuncs_min_240 import *
from address_data import *
import pandas as pd
import feather as ft

################ 因子计算结果没有 '600485.SH'（停牌）

# 先验证分钟行情数据的时间范围,分钟和日范围
files = os.listdir(add_min_file)
res = []
for filename in files:
    df = ft.read_dataframe(add_min_file+filename, nthreads=100)
    ls = list(df['date'])
    res = list(set(res+ls))  #验证结果,每个股票的时间都是完整的，468480条分钟数据
datetimel = sorted(res)[408000:] #从2017年开始，60480条分钟线数据，每个股票的时间也是完整的   
datel = list(set(map(lambda x : x[:10],datetimel))) # 日数据252条，20170103-20180115


# 沪深300指数成分股
code_HS300 = pd.read_excel(add_gene_file + 'data_mkt.xlsx',sheetname='HS300')
stockList = list(code_HS300['code'][:])

# 分钟线：从2017-01-03 09:31:00 至 2018-01-15 15:00:00
dateList = open(add_mintime_SerialFile).read().split('\n')
alpha_all(stockList, dateList, savepath=add_alpha_min_expand_file)




