# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 19:26:56 2018

@author: wuwangchuxin
"""
import os
os.chdir('D:/yh_min-mfactors')
from poss_data_format import *
from address_data import *
import feather as ft
import pandas as pd
import pickle

# stockList
code_HS300 = pd.read_excel(add_gene_file + 'data_mkt.xlsx',sheetname='HS300')
stockList = list(code_HS300['code'][:])
stockList.remove('600485.SH')  #该股票停牌 没有数据
# dateList
dateList = open(add_mintime_SerialFile).read().split('\n')

files = os.listdir(add_min_file)
for num in [1,60,120,180,240]:
    return_min = pd.DataFrame(dateList,columns={'date'})
    for filename in files:
        stockname = filename[2:8] +'.'+filename[0:2]
        if stockname in stockList:
            df = ft.read_dataframe(add_min_file+filename, nthreads=100)
            if len(df)>=60720:
                df = df.iloc[-60720:,:]
            if num == 1:
                df['return_num'] = (df['close'] - df['preClose'])*100/df['preClose']
            else:
                df['shift_num'] = df['close'].shift(num)
                df['return_num'] = (df['close']-df['shift_num'])*100/df['shift_num']
            return_min = pd.merge(return_min,df[['date','return_num']],on = 'date',how='left')
            return_min.rename(columns={'return_num':stockname},inplace = True)
            n=n+1
    return_min.to_csv(add_stock_return_min+'return_min_%s.csv'%num)






