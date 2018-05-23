# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 21:08:38 2018

@author: wuwangchuxin
"""

## 短周期量价因子研究
# 原始因子计算文件：aa_alphaFuncs_origin.py
# 步骤文件：aa_procedure_for_words.py
# 地址文件：address_data.py
# 函数文件：functions.py

#第一步：计算因子值
#分钟线：2017-01-01至2018-01-15，缺少2018-01-04 和 2018-01-05日的行情数据；   
#       其次，600485.SH'一直停牌没有数据；
# alphaFuncs_min.py,cal_min.py 
# alpha_min_expand.py 因子计算回溯口径为 *240 或者 *60
#日线：2016-01-01至2018-01-15,日行情虽然有2018-01-04 和 2018-01-05日的行情数据，
#    但是为了和分钟数据保持一致，所以没有选取这两日的行情数据。
# alphaFuncs_day.py,cal_day.py

# 第二步：标准化
# 文件：standardizing_day.py 和 standardizing_min.py

# 第三步：读取风格因子
# 文件：style_factors.py

# 第四步：计算日收益率
# 文件：return_day.py
# 文件：return_min.py

# 第五步：计算行业和风格中性，中性后的因子值和因子收益率，然后计算
# 日线：single_factors_test_day.py 

# 分钟线：single_factors_test_min.py
# 因为计算效率的原因，使用matlab处理：
# 函数文件：alpha_filename.m;
# 计算残差：matlab_for_factor_residvalue.m
# 计算IR值：factor_return_IR.m
# 保存为csv文件：save_csv.m



# 剩余的文件：
# HS300_weight.py
# IC_value_day.py
# IC_value_min.py
# mfmsolver.py
# posses_stylefactors_matlab.py
# zz_quit_computing_ic.py
# zz_quit_Hour_profit_computing.py

