import pandas as pd
import feather as ft
import pickle
import os

addr_origin = 'G:/short_period_mf/'

addr_codes = 'C:/Users/wuwangchuxin/Desktop/yinhua_min/data/data_mkt.xlsx'
addr_mkt = 'G:/1m_data/1/'
addr_8h_return = r'G:/short_period_mf/return_8_hours/'

addr_netual_factors = 'G:/short_period_mf/netual_process/'
addr_mean_alpha = 'G:/short_period_mf/mean_alpha/'

addr_IC_value = 'G:/short_period_mf/IC_value/'

##计算每个股票往前8小时的滚动收益率
def cal_8h_return(nhours=8):
    code_HS300 = pd.read_excel(addr_codes,sheetname='HS300')
    stockList = list(code_HS300['code'][:])
    mkt_files = list(map(lambda x:x[-2:]+x[:6]+'.feather',stockList))
    for file in mkt_files:
    #    file = 'SH600000.feather'
        data = ft.read_dataframe(addr_mkt+file)
        hour_data_grouped = data.groupby(data.date.apply(lambda s:s[:-6]))
        hour_data = hour_data_grouped['close','amount'].agg({'hour_vwap':\
                                 lambda df:sum(df.close * df.amount)/df.amount.sum()})
        hour_data = hour_data.iloc[:,0]
        hour_data2 = hour_data.shift(nhours)
        rate_lst = []
        for i in range(len(hour_data)-nhours):
            rate = (hour_data[i+nhours]-hour_data2[i+nhours])/hour_data2[i+nhours]
            rate_lst.append(rate)
        rate_df = pd.DataFrame(rate_lst,columns = ['rate_%s'%nhours],index = hour_data.index[nhours:])
        rate_df['code'] = file[:nhours]
        output = open(addr_8h_return+'return_%s_'%nhours+file[:nhours]+'.pickle','wb')
        pickle.dump(rate_df,output)
        output.close()
    return 0

# 汇总到一个 matrix
def return_matrix():
    stock_return = os.listdir(addr_8h_return)
    all_return = pd.DataFrame()
    for sr in stock_return:
    #    sr = 'return_8_SH600000.pickle'
        s_return = pd.read_pickle(addr_8h_return+sr)
        mid_return = pd.DataFrame(list(s_return.loc[:,'rate_8']),index=s_return.index,columns={sr[9:17]})
        if sr == 'return_8_SH600000.pickle':
            all_return = mid_return
        else:
            all_return = pd.concat([all_return,mid_return],axis=1)
    output = open(addr_origin+'all_return.pickle','wb')
    pickle.dump(all_return,output)
    output.close()
    return 0

# 利用每分钟的因子值，求沪深300成分股在每个小时内的因子值的均值
def mean_alpha_hour():
    alpha_neutral = os.listdir(addr_netual_factors)
    for an in alpha_neutral:
    #    an = 'netual_alpha_001.pickle'
        alpha_ne = pd.read_pickle(addr_netual_factors+an)
        alpha_ne=alpha_ne.melt(id_vars='code')
        alpha_ne=alpha_ne.pivot(index='variable', columns='code', values='value')
        res = alpha_ne.groupby(lambda alpha_ne: alpha_ne[:13]).mean()  
        output = open(addr_mean_alpha+'mean_alpha_'+an[13:16]+'.pickle','wb')
        pickle.dump(res,output)
        output.close()
    return 0

# 处理成和因子收益矩阵一样的格式 包括列名和列的顺序
def possess_return_format():
    stocks_return = pd.read_pickle(addr_origin+'all_return.pickle')   #  收益率矩阵
    stocks_return = stocks_return[stocks_return.index>='2017-01-03 09']
    stocks_return.drop('SH600485',axis=1, inplace=True) # 计算因子没有得到SH600485
    stocks_return.columns = list(map(lambda x : x[2:]+'.'+x[:2],stocks_return.columns)) #和因子矩阵列名保持一致
    mean_al_tmp = pd.read_pickle(addr_mean_alpha+maf)
    mean_al_tmp.columns
    stocks_return.to_csv(addr_origin+'stocks_return.csv',columns=mean_al_tmp.columns)
    stocks_return = pd.read_csv(addr_origin+'stocks_return.csv',index_col = 0)
    output = open(addr_origin+'stocks_return.pickle','wb')
    pickle.dump(stocks_return,output)
    output.close()    
    return 0

#下面是计算IC的代码
# 对时间数据进行遍历，计算每个小时的所有股票的因子均值和未来8个小时所有股票的收益率的相关系数。
# 遍历完成后，可以得到每个因子的IC时间序列。
def cal_IC():
    stocks_return = pd.read_pickle(addr_origin+'stocks_return.pickle')
    mean_alpha_files = os.listdir(addr_mean_alpha)
    res_IC = pd.DataFrame(index=stocks_return.index,\
                          columns = list(map(lambda x : x[5:14],mean_alpha_files)))
    res_IC.columns = list(map(lambda x : x[5:14],mean_alpha_files))
    for maf in mean_alpha_files:
        # maf = 'mean_alpha_001.pickle'
        mean_al = pd.read_pickle(addr_mean_alpha+maf)
        mid_IC = pd.DataFrame(columns=['alpha_factors','date','IC'])   
        for nn in range(len(mean_al)):
            mid_IC = mean_al.iloc[nn,:].corr(stocks_return.iloc[nn,:])
            res_IC.iloc[nn,res_IC.columns == maf[5:14]] = mid_IC
    output = open(addr_IC_value+'IC_value.pickle','wb')
    pickle.dump(res_IC,output)
    output.close()   
    return 0

IC_val = pd.read_pickle(addr_IC_value+'IC_value.pickle')
IC_val.to_csv(addr_IC_value+'IC_value.csv')


#mean_all = pd.DataFrame(columns=['alpha_factors','datetime','mean_factors'])
#mean_alpha_files = os.listdir(addr_mean_alpha)
#for maf in mean_alpha_files:
#    # maf = 'mean_alpha_001.pickle'
#    mean_al = pd.read_pickle(addr_mean_alpha+maf)
#    mid_df = pd.DataFrame(columns=['alpha_factors','datetime','mean_factors'])   
#    mid_df['datetime'] =mean_al.index
#    mid_df['alpha_factors'] =maf[5:14]
#    mid_df['mean_factors'] = list(mean_al.mean(axis=1))
#    mean_all = pd.concat([mean_all,mid_df])
#output = open(r'G:\short_period_mf\mean_alpha\mean_all.pickle','wb')
#pickle.dump(mean_all,output)
#output.close() 

#test = pd.read_pickle(r'G:\short_period_mf\mean_alpha\mean_all.pickle')

#未来8个小时所有股票的收益率
#mean_return8 = pd.DataFrame(columns=['datetime','mean_return'])
#mean_return8_files = os.listdir(r'G:\short_period_mf\return_8_hours')
#for mrf in mean_return8_files:
#    mean_mrf = pd.read_pickle(r'G:\short_period_mf\return_8_hours\%s'%mrf)
#    mid2_df = pd.DataFrame(columns=['datetime','mean_return'])   
#    mid2_df['datetime'] =mean_mrf.index
#    mid2_df['mean_return'] = list(mean_mrf['rate_8'])
#    if mrf == 'return_8_SH600000.pickle':
#        mean_return8 = mid2_df
#    else:
#        mean_return8 = pd.merge(mean_return8,mid2_df,on='datetime',how='outer')
#mean_return8.index = mean_return8['datetime']
#mean_return8.drop('datetime',axis=1, inplace=True)
#res_return8 = pd.DataFrame(columns=['datetime','mean_return'])
#res_return8['datetime'] = mean_return8.index
#res_return8['mean_return'] = list(mean_return8.mean(axis=1))
#output = open(r'G:\short_period_mf\return_8_hours\mean_return8.pickle','wb')
#pickle.dump(res_return8,output)
#output.close() 

# 收益率乘以100
#res2_return8 = res_return8
#res2_return8['mean_return'] = res2_return8['mean_return'].apply(lambda x:x*100)
#output = open(r'G:\short_period_mf\return_8_hours\mean_%return8.pickle','wb')
#pickle.dump(res2_return8,output)
#output.close() 
    
      
        
        
        
#mean_all = pd.read_pickle(r'G:\short_period_mf\mean_alpha\mean_all.pickle')
#res_return8 = pd.read_pickle(r'G:\short_period_mf\return_8_hours\mean_return8.pickle')
#res2_return8 = pd.read_pickle(r'G:\short_period_mf\return_8_hours\mean_%return8.pickle')

# 
#result1 = pd.merge(mean_all,res_return8,on='datetime',how='inner')
#result2 = pd.merge(mean_all,res2_return8,on='datetime',how='inner')
#
#result1 = result1.rename(columns={'mean':'mean_factors'})
#result2 = result2.rename(columns={'mean':'mean_factors'})
#
#result1_grouped = result1.groupby([result1['alpha_factors'],result1['datetime'].apply\
#                                     (lambda x : x[:10])])
#    #'alpha_factors','datetime',
#IC_res1 = pd.DataFrame(columns=['alpha_factors','date','IC'])
#for a,b in result1_grouped:
#    mid_IC = pd.DataFrame(columns=['alpha_factors','date','IC'])
#    mid_IC.loc[0,'alpha_factors']=a[0]
#    mid_IC.loc[0,'date']=a[1]
#    mid_IC.loc[0,'IC']=b['mean_factors'].corr(b['mean_return'])
#    IC_res1 = pd.concat([IC_res1,mid_IC])
#output = open(r'G:\short_period_mf\IC_value\IC_value1.pickle','wb')
#pickle.dump(IC_res1,output)
#output.close() 
#IC_res1.to_csv(r'G:\short_period_mf\IC_value\IC_value.csv')

#result2_grouped = result2.groupby([result2['alpha_factors'],result2['datetime'].apply\
#                                     (lambda x : x[:10])])
#IC_res2 = pd.DataFrame(columns=['alpha_factors','date','IC'])
#for a,b in result2_grouped:
#    mid_IC2 = pd.DataFrame(columns=['alpha_factors','date','IC'])
#    mid_IC2.loc[0,'alpha_factors']=a[0]
#    mid_IC2.loc[0,'date']=a[1]
#    mid_IC2.loc[0,'IC']=b['mean_factors'].corr(b['mean_return'])
#    IC_res2 = pd.concat([IC_res2,mid_IC2])
#output = open(r'G:\short_period_mf\IC_value\IC_value2.pickle','wb')
#pickle.dump(IC_res2,output)
#output.close() 




#IC_v1 = pd.read_pickle(r'G:\short_period_mf\IC_value\IC_value1.pickle')
#IC_v2 = pd.read_pickle(r'G:\short_period_mf\IC_value\IC_value2.pickle')




#    hour_data = hour_data_grouped['close','amount'].agg({'hour_vwap':\
#                             lambda df:sum(df.close * df.amount)/df.amount.sum()})

#lambda_fuc = lambda df:(pd.Series(df.mean_factors)).corr((pd.Series(df.mean_return)))
#IC_data1 = result1_grouped['mean_factors','mean_return'].agg({'day_ic':lambda_fuc}) 


#test = result1.head()
#
#
#test['mean'].corr(test['mean_return'])
#s1=pd.Series(test['mean'])
#s2=pd.Series(test['mean_return'])
#s1.corr(s2)
#
#import numpy as np
#np.cov(test['mean'],test['mean_return'])
# test.corr()  
#
#
#lambda_fuc(test)
#
#
#
#c=[2,4,6,8,10,12,14,16,18]
#    d= [i*2 for i in c]
#    print d
#    d[0]=3 # 修改d[0]的值
#    s1=Series(c) #转为series类型
#    s2=Series(d)
#    corr=s1.corr(s2) #计算相关系数
#    print corr



