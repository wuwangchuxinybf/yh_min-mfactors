import pandas as pd
import numpy as np

data = pd.read_pickle('Data/SH600000.pickle')
#先计算每个小时的vwap
hour_data_grouped = data.groupby(data.date.apply(lambda s:s[:-6]))
hour_data = hour_data_grouped['close','amount'].agg({'hour_vwap':lambda df:sum(df.close * df.amount)/df.amount.sum()})
hour_data = hour_data.iloc[:,0]
hour_data2 = hour_data.shift(8)
rate_lst = []
for i in range(len(hour_data)-8):
    rate = (hour_data[i+8]-hour_data2[i+8])/hour_data2[i+8]
    rate_lst.append(rate)
rate_df = pd.DataFrame(rate_lst,columns = ['rate_8'],index = hour_data.index[8:])
print(rate_df.head())
#得到的结果为:date(每个小小时)rate_8该文件下这个股票的8小时的滚动收益率

#下面是计算IC的代码















































