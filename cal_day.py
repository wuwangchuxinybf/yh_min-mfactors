# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 22:18:07 2018

@author: wuwangchuxin
"""
import os
os.chdir('D:/yh_min-mfactors')
from alphaFuncs_day import *
from address_data import *
import pandas as pd
import feather as ft

# 2018-04-02 发现 'G:\short_period_mf\trade_min.date' 文件缺少下面三个日期的数据
# 原因是原始分钟行情数据缺少，而日数据不缺少,统一按照分钟线的时间尺度进行处理
#2018-01-04
#2018-01-05
#2018-01-16

# 沪深300指数成分股
code_HS300 = pd.read_excel(add_gene_file + 'index_stockcodes.xlsx',sheetname='HS300')
stockList = list(code_HS300['code'][:])
# 日数据太大，先进行预处理
def possess_day():
    marketData = ft.read_dataframe(add_day_file+'marketData.feather')
    marketData_2016 = marketData[marketData['date']>='2016-01-01']
    # 相比于分钟线数据多了个'symbol'字段 少了个'preClose'字段）
    marketData_2s = marketData_2016[['date','symbol','open','high','low','close','preClose','amount','vwap']]
    stockList2 = list(map(lambda x : x[:6],stockList))
    marketData_res = marketData_2s[marketData_2s['symbol'].isin(stockList2)]  ### 一个用法 isin
    marketData_res.to_csv(add_day_file + 'marketData.csv',index = False)
    return 0

# 得到日期范围并创建trade_day.date文件：从2016-01-04 至 2018-01-15
def creat_dateList():  
    marketData = pd.read_csv(add_day_file + 'marketData.csv')
    dateList_day = list(set(marketData['date']))
    dateList_day = list(map(lambda x : poss_date(x),dateList_day))
    for date in ['2018-01-04','2018-01-05','2018-01-16']:
        dateList_day.remove(date)
    #然后手动复制到'G:\short_period_mf\trade_day.date'里面
    return 0

################ 因子计算结果没有 '600485.SH'（停牌）
dateList = open(add_daytime_SerialFile).read().split('\n')
alpha_all(stockList, dateList, savepath=add_alpha_day_file)