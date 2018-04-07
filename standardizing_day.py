# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 20:42:21 2018

@author: wuwangchuxin
"""
#import time
import os
os.chdir('D:/yh_min-mfactors')
from address_data import *
import numpy as np
import pandas as pd
import pickle

import statsmodels.api as sm

#start=time.clock()
def standard_progress():
    filenameList = os.listdir(add_alpha_day_file)
#    filenameList = filenameList[148:]  #alpha_149的代码名称为code
    for filename in filenameList:
        #首先对因子值进行空值删除和标准化处理
#        start=time.clock()
        data = pd.read_csv(add_alpha_day_file+filename)
        data.dropna(axis=1,how='all',inplace = True)
        data_c = data.fillna(0)
        data_b = data_c.iloc[:,1:]
        data_d = np.array(data_b)
        x_mean = data_d.mean(axis = 0)   #每一日所有股票的
        x_std = data_d.std(axis = 0)    #每一日所有股票的
        for i in range(len(data_c.columns)-1):
            for j in range(len(data_c)):  # 之前是 len(data_c)-1
                if data_d[j][i] > (x_mean[i]+1.65*x_std[i]):
                    data_d[j][i] = (x_mean[i]+1.65*x_std[i])
                elif data_d[j][i] < (x_mean[i]-1.65*x_std[i]): # 之前是 x_mean[i]+1.65*x_std[i]
                    data_d[j][i] = (x_mean[i]-1.65*x_std[i])                   
        data_d=pd.DataFrame(data_d,index=list(data_c['symbol']),columns=list(data_c.columns)[1:])
        data_d.reset_index(inplace=True)
        data_d = data_d.rename(columns={'index':'code'})
        # 存到移动硬盘里
        output = open(add_alpha_day_stand + 'standard_%s.pickle'%filename[:9],'wb')
        pickle.dump(data_d,output)
        output.close()
#        end = time.clock()
    return None


#standard_alpha_001 = pd.read_pickle(r'G:\short_period_mf\alpha_day_stand\standard_alpha_001.pickle')




#test2 = pd.read_pickle(r'G:\short_period_mf\alpha_min_stand\standard_alpha_001.pickle')
#test3 = pd.read_csv(r'G:\short_period_mf\alpha_min\alpha_001.csv')
#stockList
#sl = test3.iloc[:,0]
    
#
#def Netual_process(alpha_data,industry,saf):
#    new_data = pd.merge(alpha_data,industry,on = ['code'])
#    new_data2 = pd.DataFrame(new_data.code)
#    for i in range(len(new_data.columns.tolist())-1):
#        y = new_data.iloc[:,i+1].as_matrix()
#        X = new_data.iloc[:,-30:].as_matrix()
#        model = sm.OLS(X,y)
#        results = model.fit()
#        Betas = results.params #这里没有常数项，所有参数均为回归系数
#        new_factors = pd.DataFrame(y - X.dot(Betas.T))
#        new_data2 = pd.concat([new_data2,new_factors],axis = 1)
#    output = open(r'G:\short_period_mf\netual_process\netual_%s'%saf[-16:],'wb')
#    pickle.dump(new_data2,output)
#    output.close()
#    return None
#
#def IC_computing(path,industry):
#    data = pd.read_pickle(path)
#    factors = Netual_process(data,industry)
#    IC = minuteReturn.corr(factors)
#    output = open(r'G:\short_period_mf\ic_value\ic_%s'%saf[-16:],'wb')
#    pickle.dump(IC,output)
#    output.close()    
#    return None

#industry2=pd.read_pickle(r'C:\Users\wuwangchuxin\Desktop\yinhua_min\data\industry.pkl')
#industry3 = industry2.drop_duplicates()
#standard_alpha = os.listdir(r'G:\short_period_mf\alpha_min_stand')
#for saf in standard_alpha:
#    path = r'G:\short_period_mf\alpha_min_stand\%s'%saf
#    IC_computing(path,industry)
#
#
#for saf in standard_alpha:
#    alpha_d = pd.read_pickle(r'G:\short_period_mf\alpha_min_stand\%s'%saf)
#    Netual_process(alpha_d,industry3,saf)
##
#paths = os.listdir(r'G:\short_period_mf\netual_process')
#for pat in paths:
#    IC_computing(pat,industry)


#industry3.to_csv(r'C:\Users\wuwangchuxin\Desktop\industry3.csv')
#
#alpha_d2.to_csv(r'C:\Users\wuwangchuxin\Desktop\netual_alpha001_part.csv')
#alpha_d2 = alpha_d[:2]





#
#def IC_computing():
#    data = pd.read_pickle(r'G:\alpha_min_stand\standard_Alpha_001.pickle')
#    return_data = pd.read_pickle('dailyreturn.pickle')
#    return_data = return_data.reset_index()
#    new_data = pd.merge(data,return_data,on = ['code'])
#    dailyReturn = new_data.daily_return
#    factor = new_data.ix[:,0:-1].mean(1)
##    print(factor)
#    IC = dailyReturn.corr(factor)
##    print(IC)
#    return None
#
#
#def dfEWREGBETA(df1, sr, n, halflife=60):
#	df1 = df1.ewm(halflife).mean()
#	sr2 = sr.ewm(halflife).mean()
#    condition_1 = isinstance(sr, np.ndarray)
#    condition_2 = isinstance(sr, pd.core.series.Series)
#    temp = df1.copy()
#    if condition_1:
#        temp.rolling(n).apply(lambda y: stats.linregress(x=sr, y=y)[0])
#    if condition_2:
#        for i in range(0, len(df1) - n):
#            temp.iloc[i:i + n, :].apply(lambda y: stats.linregress(x=sr.iloc[i:i + n], y=y)[0])
#    return temp



















