# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 21:08:38 2018

@author: wuwangchuxin
"""

## 短周期量价因子研究
# 步骤文件：procedure_for_words.py
# 地址文件：address_data.py
# 函数文件：functions.py

#第一步：计算因子值
#分钟线：2017-01-01至2018-01-15，缺少2018-01-04 和 2018-01-05日的行情数据；   
#       其次，600485.SH'一直停牌没有数据；
# alphaFuncs_min.py,cal_min.py 
#日线：2016-01-01至2018-01-15,日行情虽然有2018-01-04 和 2018-01-05日的行情数据，
#    但是为了和分钟数据保持一致，所以没有选取这两日的行情数据。
# alphaFuncs_day.py,cal_day.py

# 第二步：标准化
# 文件：standardizing_day.py 和 standardizing_min.py

# 第三步：读取风格因子
# 文件：style_factors.py

# 第四步：计算日收益率
# 文件：return_day.py

# 第五步：计算行业和风格中性，中性后的因子值和因子收益率，然后计算
# 文件：single_factors_test_day.py 和 single_factors_test_min.py 回归





