# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 18:25:06 2018

@author: wuwangchuxin
"""

#add_origin_file = 'G:/1m_data/'

add_gene_file = 'G:/short_period_mf/'  #生成的数据地址
add_day_file = 'G:/1m_data/mkt_daybar/'  #日行情数据地址
add_daytime_SerialFile = 'G:/short_period_mf/trade_day.date'  #日时间序列文件
add_alpha_day_file = 'G:/short_period_mf/alpha_day/' # 日alpha因子文件地址
add_alpha_day_stand = 'G:/short_period_mf/alpha_day_stand/' #标准化日alpha因子文件地址

add_min_file = 'G:/1m_data/1/'  #分钟行情数据地址
add_mintime_SerialFile='G:/short_period_mf/trade_min.date' #分钟时间序列文件
add_alpha_min_file = 'G:/short_period_mf/alpha_min/' # 分钟alpha因子文件地址
add_alpha_min_stand = 'G:/short_period_mf/alpha_min_stand/' #标准化分钟alpha因子文件地址

add_style_factors = 'G:/1m_data/Barra/'  # 风格因子原始数据
add_Nstyle_factors = 'G:/short_period_mf/style_factors/' # 风格因子处理后数据

add_resid_value_day = 'G:/short_period_mf/resid_value_day/' # 单因子残差值
add_resid_value_min = 'G:/short_period_mf/resid_value_min/' # 单因子残差值
add_factor_freturn = 'G:/short_period_mf/factor_freturn_day/' #单因子收益

add_factor_freturn_IR = 'G:/short_period_mf/factors_return_pyear_IR/' #因子年化收益和IR值

add_alpha_min_csv = 'G:/short_period_mf/alpha_min_stand_matlab/' #因子值存入csv然后用MATLAB处理