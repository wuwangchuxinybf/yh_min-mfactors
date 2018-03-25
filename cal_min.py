# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 21:49:28 2018

@author: wuwangchuxin
"""

import os
os.chdir(r'D:\yh_min-mfactors')
from alphaFuncs import *
import pandas as pd

################ 因子计算结果没有 '600485.SH'
minute_file_path = 'G:\\1m_data\\1\\'
timeSerialFile=r'C:\Users\wuwangchuxin\Desktop\yinhua_min\data\trade.date'

# 沪深300指数成分股
code_HS300 = pd.read_excel(r'C:\Users\wuwangchuxin\Desktop\yinhua_min\data\data_mkt.xlsx',\
              sheetname='HS300')
stockList = list(code_HS300['code'][:])
# 分钟线：从2017-01-03 09:31:00 至 2018-01-15 15:00:00
dateList = open(r'C:\Users\wuwangchuxin\Desktop\yinhua_min\data\trade.date').read().split('\n')
alpha_all(stockList, dateList, savepath='E:\\alpha_min\\')












