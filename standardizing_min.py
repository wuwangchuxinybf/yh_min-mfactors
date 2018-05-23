# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 20:42:21 2018

@author: wuwangchuxin
"""
#import time
import os
os.chdir('D:/yh_min-mfactors')
from functions import *
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
        print (filename)
        #首先对因子值进行空值删除和标准化处理        
        data = pd.read_csv(add_alpha_min_file+filename)
        data.dropna(axis=1,how='all',inplace = True)
        data_b = np.array(data.iloc[:,1:])
        x_mean = np.nanmean(data_b,axis=0).reshape(1,-1)  
        x_std = np.nanstd(data_b,axis=0).reshape(1,-1)
        data_std = (data_b - x_mean)/x_std
        x_std_df = np.tile(x_std,(299,1))
        data_b[data_std>3] = 3*x_std_df[data_std>3]
        data_b[data_std<-3] = -3*x_std_df[data_std<-3]
        x_mean2 = np.nanmean(data_b,axis=0).reshape(1,-1)
        x_std2 = np.nanstd(data_b,axis=0).reshape(1,-1)
        data_b[np.isnan(data_b)] = np.tile(x_mean2,(299,1))[np.isnan(data_b)]
        data_c = (data_b - x_mean2)/x_std2       
        data_c=pd.DataFrame(data_c,index=list(data['code']),columns=list(data.columns)[1:])
        data_c.reset_index(inplace=True)
        data_c = data_c.rename(columns={'index':'code'})
        # 存到移动硬盘里
        data_c.to_csv(add_alpha_min_stand + 'standard_%s.csv'%filename[:9],index=False)
    return 0


#standard_alpha_001 = pd.read_pickle(add_alpha_min_stand + 'standard_alpha_001.pickle')















