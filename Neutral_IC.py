# -*- coding: utf-8 -*-

import os
os.chdir('D:/yh_min-mfactors')
from poss_data_format import *
from address_data import *
import pandas as pd
import statsmodels.api as sm


# 某一时间截面，所有个股的收益对所有个股的各个因子进行多元回归，得到因子在这一时间截面的收益率；
# 最后得到关于每一个因子收益率的时间序列数据
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
#        
#
#dateList = open(add_daytime_SerialFile).read().split('\n')
#
#alpha_001 = pd.read_csv(r'G:/short_period_mf/alpha_day/alpha_001.csv')
#alpha_001['symbol'] = alpha_001['symbol'].apply(lambda x : poss_symbol(x))
#day_list = list(alpha_001.columns)[1:]
#
#Beta['date']
#
#Beta = pd.read_csv(add_Nstyle_factors + 'Beta.csv')
#
#
## 因子数据截止到2017-12-06日
#style_filenames = os.listdir(add_Nstyle_factors)
#style_filenames.pop(-3)  # 不要NLSize数据
#style_list = []
#for sfilename in style_filenames:
#    style_list.append(sfilename[:-4])
#    names = locals()
#    names[sfilename[:-4]] = pd.read_csv(add_Nstyle_factors+sfilename)
#    names[sfilename[:-4]] = eval(sfilename[:-4])[eval(sfilename[:-4])['date']>='2017-01-01']
    
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

#    num_mint = alpha_data.shape[1]
#    num_inds = industry.shape[1]
#
#    X = data.iloc[:, 1:num_mint]
#    y = data.iloc[:, num_mint:num_mint+num_inds]
#    X = X.apply(lambda x:resid(x, y))
#    X['code'] = alpha_data['code']
##    output = open('G:/short_period_mf/netual_process/netual_%s'%saf[-16:],'wb') 
#    output = open('G:/short_period_mf/netual_day_process/netual_%s'%saf[-16:],'wb')
#    pickle.dump(X,output)
#    output.close()
#    return X

#test = pd.read_pickle(r'G:\short_period_mf\netual_day_process\netual_alpha_001.pickle')
#standard_alpha = os.listdir(r'G:/short_period_mf/alpha_min_stand')

standard_alpha = os.listdir(add_alpha_day_stand)
for saf in standard_alpha:
    alpha_d = pd.read_pickle(add_alpha_day_stand + saf)
    factor_data = Neutral_process(alpha_d,saf)
    X = industry
    for date in factor_data['date']:
        Y = factor_data[factor_data['date'] == date]  # 每个时间截面的因子值
        for sfile in style_list:
            mid_sd = eval(sfile)
            X = X.append(mid_sd[mid_sd['date'] == date])
        







    data = pd.merge(alpha_data, industry, on=['code']).dropna()
    data = data.melt(id_vars='code')
    data = data.pivot(index='variable', columns='code', values='value')