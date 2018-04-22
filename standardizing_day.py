# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 20:42:21 2018

@author: wuwangchuxin
"""
#import time
import os
os.chdir('D:/yh_min-mfactors')
from address_data import *
from functions import *
#import numpy as np
import pandas as pd
#import pickle
#import statsmodels.api as sm

# 处理思路：先删除整列全为nan的列，然后先不填nan值，按照列（截面所有样本）求因子均值和方差，
#           然后按列大于3倍或者小于-3倍标准差的极值令其等于该3倍标准差，再接着求去除极值后的
#           按列的均值和标准差，将nan值填充为均值，然后进行z-score标准化；
# 先去极值再标准化；
#start=time.clock()
def standard_progress():
    filenameList = os.listdir(add_alpha_day_file)
#    filenameList = filenameList[148:]  #alpha_149的代码名称为code
    for filename in filenameList:
        #首先对因子值进行空值删除和标准化处理
#        start=time.clock()
        print (filename)
        data = pd.read_csv(add_alpha_day_file+filename)
        data.dropna(axis=1,how='all',inplace = True)
        data_b = data.iloc[:,1:]
        data_d = stand_fac(data_b)
#        x_mean = data_b.mean()   #每一日所有股票的 默认 axis = 0
#        x_std = data_b.std()    #每一日所有股票的     
#        for j in range(len(data_b.columns)): 
#            for i in range(len(data_b)):
#                if not np.isnan(data_b.iloc[i,j]):
#                    if (data_b.iloc[i,j]-x_mean[j])/x_std[j] > 3:
#                        data_b.iloc[i,j] = 3
#                    elif (data_b.iloc[i,j]-x_mean[j])/x_std[j] < -3:
#                        data_b.iloc[i,j] = -3 #(x_mean[i]-3*x_std[i])   
#        x_mean2 = np.array(data_b.mean())
#        x_std2 = np.array(data_b.std())
#        data_c = pd.DataFrame(index = data_b.index,columns = data_b.columns)
#        for k in range(len(data_b.columns)):
#            data_c.iloc[:,k] = data_b.iloc[:,k].fillna(x_mean2[k])
#        data_d = np.array(data_c)        
#        data_d = (data_d-x_mean2)/x_std2     
        data_d=pd.DataFrame(data_d,index=list(data['symbol']),columns=list(data_c.columns))
        data_d.reset_index(inplace=True)
        data_d = data_d.rename(columns={'index':'code'})
        # 存到移动硬盘里
        data_d.to_csv(add_alpha_day_stand + 'standard_%s.csv'%filename[:9],index=False)
#        output = open(add_alpha_day_stand + 'standard_%s.pickle'%filename[:9],'wb')
#        pickle.dump(data_d,output)
#        output.close()
#        end = time.clock()
    return None


















