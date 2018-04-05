# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 22:18:07 2018

@author: wuwangchuxin
"""
import os
os.chdir('D:/yh_min-mfactors')
from alphaFuncs_day_plus import *
import pandas as pd
import feather as ft

day_file_path = 'G:/1m_data/'
timeSerialFile = 'G:/short_period_mf/trade_day.date'

# 2018-04-02 发现 'G:\short_period_mf\trade.date' 文件缺少下面三个日期的数据
# 原因是原始分钟行情数据缺少，而日数据不缺少,统一按照分钟线的时间尺度进行处理
#2018-01-04
#2018-01-05
#2018-01-16

# 沪深300指数成分股
code_HS300 = pd.read_excel('G:/short_period_mf/data_mkt.xlsx',\
              sheetname='HS300')
stockList = list(code_HS300['code'][:])
# 日数据太大，先进行预处理
def possess_day():
    marketData = ft.read_dataframe('G:/1m_data/marketData.feather')
    marketData_2017 = marketData[marketData['date']>='2017-01-01']
    # 相比于分钟线数据多了个'symbol'字段 少了个'preClose'字段）
    marketData_2s = marketData_2017[['date','symbol','open','high','low','close','preClose','amount','vwap']]
    stockList2 = list(map(lambda x : x[:6],stockList))
    marketData_res = marketData_2s[marketData_2s['symbol'].isin(stockList2)]  ### 一个用法 isin
    marketData_res.to_csv('G:/1m_data/marketData.csv')
    return 0

#df = pd.read_csv('G:/1m_data/marketData.csv')
#test = df[df['date']=='2018/1/5']

# 得到日期范围并创建trade_day.date文件：从2017-01-03 至 2018-01-15
def creat_dateList():
    dateList_min = open('G:/short_period_mf/trade.date').read().split('\n')
    dateList_day = list(set(map(lambda x : x[:10],dateList_min)))
    #然后手动复制到'G:\short_period_mf\trade_day.date'里面
    return 0

################ 因子计算结果没有 '600485.SH'（停牌）
dateList = open(timeSerialFile).read().split('\n')
alpha_all(stockList, dateList, savepath='G:/short_period_mf/alpha_day/')
