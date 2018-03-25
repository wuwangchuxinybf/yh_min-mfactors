# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 21:13:10 2018

@author: wuwangchuxin
"""

import feather as ft
import pickle
import pandas as pd

df = ft.read_dataframe(r'G:\1m_data\1\SH600000.feather')
output = open(r'G:\1m_data\1\SH600000.pickle','wb')
pickle.dump(df,output)
output.close()


dfa = pd.read_pickle(r'G:\short_period_mf\netual_process\netual_alpha_001.pickle')



test = pd.read_csv(r'E:\alpha_min\alpha_002.csv')
test2 = test.iloc[:,:5]

ts = list(test.columns)
timeSerialList


dfs = pd.read_pickle(r'G:\short_period_mf\alpha_min_stand\standard_alpha_001.pickle')

dfn = pd.read_pickle(r'G:\short_period_mf\netual_process\netual_alpha_001.pickle')














