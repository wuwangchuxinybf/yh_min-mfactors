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
addr_ICIR_value = 'G:/short_period_mf/ICIR/'

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
    maf = 'mean_alpha_001.pickle'
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

#IC_val = pd.read_pickle(addr_IC_value+'IC_value.pickle')
#IC_val.to_csv(addr_IC_value+'IC_value.csv')

# 计算不同时间尺度的因子IC值和ICIR值
def cal_ICIR():
    IC_val = pd.read_pickle(addr_IC_value+'IC_value.pickle')
    IC_val = IC_val.astype(float)
    IC_day = IC_val.groupby(lambda x : x[:10]).mean()
    IC_day.to_csv(addr_IC_value+'IC_day.csv')
    IC_month = IC_val.groupby(lambda x : x[:7]).mean()
    IC_month.to_csv(addr_IC_value+'IC_month.csv')
    ICIR_min = IC_val.apply(lambda x:x.mean()/x.std())
    ICIR_day = IC_day.apply(lambda x:x.mean()/x.std())
    ICIR_month = IC_month.apply(lambda x:x.mean()/x.std())
    ICIR_res = pd.DataFrame([ICIR_min,ICIR_day,ICIR_month],\
                            index={'ICIR_min','ICIR_day','ICIR_month'}).T
    ICIR_res.to_csv(addr_ICIR_value+'ICIR_res.csv')

























