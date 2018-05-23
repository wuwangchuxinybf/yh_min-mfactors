# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 21:04:41 2018

@author: wuwangchuxin
"""
import pandas as pd
import numpy as np
import os

fname = os.listdir(r'G:\short_period_mf\style_factors')
for fn in fname:
    stylef = pd.read_csv('G:/short_period_mf/style_factors/'+fn)
    stylef.drop(['600485.SH'],axis=1,inplace=True)
    stylef.set_index('date',inplace=True)
    res_style = np.array(stylef.T)
    np.savetxt('G:/short_period_mf/alpha_min_stand_matlab/'+fn,res_style,delimiter=',')
    