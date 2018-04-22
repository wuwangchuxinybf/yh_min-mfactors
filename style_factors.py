# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 20:56:15 2018

@author: wuwangchuxin
"""

import os
os.chdir('D:/yh_min-mfactors')
from address_data import *
import pandas as pd
from functions import *
import numpy as np

code_HS300 = pd.read_excel(add_gene_file + 'data_mkt.xlsx',sheetname='HS300')
stockList = list(code_HS300['code'][:])

# 风格因子没有标准化
def poss_style_factors(end_date='2017-01-01')
    style_filenames = os.listdir(add_style_factors)
    style_filenames.pop(-3) # 不要NLSize数据
    for filename in style_filenames:
        print (filename)
        df = pd.read_csv(add_style_factors+filename)
        col = list(df.columns)
        col[1:] = map(add_exchange,list(map(poss_symbol,col[1:])))
        col[0] = 'date' 
        df.columns = col
        df = df[list(['date']+stockList)]
        df = df[df['date']>=end_date]
        df.set_index('date',inplace = True)
        df = df.T
        df.dropna(axis=1,how='all',inplace = True)        
        df_res = stand_fac(df)
        df_res = df_res.T
        df_res=pd.DataFrame(df_res,index=list(df.columns),columns=df.index)
        df_res.reset_index(inplace=True)
        df_res = df_res.rename(columns={'index':'date'})
        mid_name = filename[:filename.index('_')]
        df_res.to_csv(add_Nstyle_factors + '%s.csv'%mid_name,index = False)























































