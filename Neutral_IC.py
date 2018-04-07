# -*- coding: utf-8 -*-

import os
os.chdir('D:/yh_min-mfactors')
from poss_data_format import *
from address_data import *
import pandas as pd
import statsmodels.api as sm
import numpy as np

# 某一时间截面，所有个股的收益对所有个股的各个因子进行多元回归，
# 得到某个因子在某个时间个股的残差值，数据量191*227*300，得到有效因子
# 然后对每个截面求得预测收益和实际收益的相关系数，即IC(t)值，最后得到一个时间序列的IC值
# 对IC值进行T检验

# 第一步 读取行业数据和个股收益率
code_HS300 = pd.read_excel(add_gene_file + 'data_mkt.xlsx',sheetname='HS300')
stockList = list(code_HS300['code'][:])
industry = pd.read_pickle\
    (add_gene_file + 'industry.pkl').drop_duplicates()
industry = industry[industry['code'].isin(stockList)]
industry.index = industry['code']
industry.drop(['code'],axis = 1,inplace = True)
industry = industry.T
industry.reset_index(inplace = True)
industry.rename(columns={'index':'date'},inplace = True)

#return_data = pd.read_pickle\
#    (add_gene_file + 'dailyreturn.pickle').rename(columns={'symbol':'code'})

# 第二步 读取风格因子数据
# 因子数据截止到2017-12-06日'
style_filenames = os.listdir(add_Nstyle_factors)
style_list = list(map(lambda x : x[:-4],style_filenames))
for sfilename in style_filenames:
    names = locals()
    names[sfilename[:-4]] = pd.read_csv(add_Nstyle_factors+sfilename)
   
# 第三步 因子值回归
def resid(x, y):
    return sm.OLS(x, y).fit().resid
    
def Neutral_process(alpha_data, saf):
    alpha_data['code'] = alpha_data['code'].apply(lambda x:add_exchange(poss_symbol(x)))
    mid_columns = ['code'] + [x for x in list(alpha_data.columns)[1:] \
                  if x >='2017-01-01'and x<='2017-12-06']
    alpha_data = alpha_data.loc[:,mid_columns]
    alpha_data.index = alpha_data['code']
    alpha_data.drop(['code'],axis = 1,inplace = True)
    alpha_data = alpha_data.T
    alpha_data.reset_index(inplace = True)
    alpha_data.rename(columns={'index':'date'},inplace = True)
    return alpha_data

standard_alpha = os.listdir(add_alpha_day_stand)
for saf in standard_alpha:   
    alpha_d = pd.read_pickle(add_alpha_day_stand + saf)
    factor_data = Neutral_process(alpha_d,saf)
    df_resid=pd.DataFrame(index=stockList,columns =factor_data['date'])
    n=0
    for date in factor_data['date']:
        X = industry
        Y = factor_data[factor_data['date'] == date] # 每个时间截面的因子值
        Y = Y.loc[:,stockList].T
        Y = np.array(Y.fillna(0))
        for sfile in style_list:
            mid_sd = eval(sfile)
            X = X.append(mid_sd[mid_sd['date'] == date])
        X = X.loc[:,stockList].T
        X = np.array(X.fillna(0))
        df_resid.iloc[:,n] = resid(Y, X)
        n=n+1
    df_resid.to_csv(add_resid_value+saf[9:18]+'_resid.csv',index = False)