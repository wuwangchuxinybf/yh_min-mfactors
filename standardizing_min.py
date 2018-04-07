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
import os

#start=time.clock()
def standard_progress():
    filenameList = os.listdir(add_alpha_min_file)
#    filenameList = filenameList[148:]  #alpha_149的代码名称为code,手动打开数据文件改为symbol
    for filename in filenameList:
        #首先对因子值进行空值删除和标准化处理
#        start=time.clock()
        data = pd.read_csv(add_alpha_min_file+filename)
        data = pd.concat([data.iloc[:,0],data.iloc[:,7:]],axis=1)
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
        output = open(add_alpha_min_stand + 'standard_%s.pickle'%filename[:9],'wb')
        pickle.dump(data_d,output)
        output.close()
#        end = time.clock()
    return None


#standard_alpha_001 = pd.read_pickle(add_alpha_min_stand + 'standard_alpha_001.pickle')


















