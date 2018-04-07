# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 20:20:33 2018

@author: wuwangchuxin
"""

def poss_symbol(symbol):
    if len(str(symbol)) == 1:
        return '00000'+str(symbol)
    elif len(str(symbol)) == 2:
        return '0000'+str(symbol)
    elif len(str(symbol)) == 3:
        return '000'+str(symbol)
    elif len(str(symbol)) == 4:
        return '00'+str(symbol)
    elif len(str(symbol)) == 5:
        return '0'+str(symbol)
    else:
        return str(symbol)
    
def poss_date(date):
    if len(date) == 10:
        return date[:4]+'-'+date[5:7]+'-'+date[8:]
    elif len(date) == 8:
        return date[:4]+'-0'+date[5]+'-0'+date[-1]
    elif date[-2] == r'/':
        return date[:4]+'-'+date[5:7]+'-0'+date[-1]
    else:
        return date[:4]+'-0'+date[5]+'-'+date[-2:]

def add_exchange(symbol):
    if symbol[:2]=='60':
        return symbol+'.SH'
    else:
        return symbol+'.SZ'