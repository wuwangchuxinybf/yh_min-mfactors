# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 20:56:15 2018

@author: wuwangchuxin
"""

import os
os.chdir('D:/yh_min-mfactors')
from address_data import *
import pandas as pd
from poss_data_format import *
import numpy as np

code_HS300 = pd.read_excel(add_gene_file + 'data_mkt.xlsx',sheetname='HS300')
stockList = list(code_HS300['code'][:])

# 风格因子没有标准化
def poss_style_factors(end_date='2017-01-01')
    style_filenames = os.listdir(add_style_factors)
    style_filenames.pop(-3) # 不要NLSize数据
    for filename in style_filenames:
        df = pd.read_csv(add_style_factors+filename)
        col = list(df.columns)
        col[1:] = map(add_exchange,list(map(poss_symbol,col[1:])))
        col[0] = 'date' 
        df.columns = col
        df = df[list(['date']+stockList)]
        df = df[df['date']>=end_date]
        df.fillna(0,inplace=True)
        
        df_d = df.iloc[:,1:]
        df_d = np.array(df_d)
        x_mean = df_d.mean(axis = 1)   #每一日所有股票的
        x_std = df_d.std(axis = 1)    #每一日所有股票的
        for i in range(len(df)):
            for j in range(len(df.columns)-1):
                if df_d[i][j] > (x_mean[i]+1.65*x_std[i]):
                    df_d[i][j] = (x_mean[i]+1.65*x_std[i])
                elif df_d[i][j] < (x_mean[i]-1.65*x_std[i]): # 之前是 x_mean[i]+1.65*x_std[i]
                    df_d[i][j] = (x_mean[i]-1.65*x_std[i]) 
        df.iloc[:,1:] = df_d
        mid_name = filename[:filename.index('_')]
        df.to_csv(add_Nstyle_factors + '%s.csv'%mid_name,index = False)




# Beta Momentum Size Earnings_Yield Volatilty Growth Value Leverage Liquidity
#                    EarnYield       ResVol           PB

#def poss_style_data(end_date='2017-01-01'):
#    style_filenames = os.listdir(add_Nstyle_factors)
#    style_filenames.pop(-3)  # 不要NLSize数据
#    for sfilename in style_filenames:       
#        mid_data = pd.read_csv(add_Nstyle_factors+sfilename)
#        mid_data = mid_data[mid_data['date']>=end_date]        
#        mid_data=mid_data.melt(id_vars='date')
#        mid_data['variable'] = mid_data['variable'].apply(lambda x : add_exchange(x))
#        mid_data=mid_data.pivot(index='variable', columns='date', values='value')
#        mid_data.reset_index(inplace = True)
#        mid_data.rename(columns={'variable':'code'},inplace = True)
#        mid_data.fillna(0,inplace = True)
#        mid_data.to_csv()
#        names = locals()
#        names[sfilename[:-4]] = mid_data

























































