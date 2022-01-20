# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 17:16:34 2022

@author: 22977
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 18:22:45 2022

@author: 22977
"""
import numpy as np
import pandas as pd
from scipy.stats import norm
import scipy.optimize as opt
import datetime
from math import * # cmath支持负数
import xlrd
import matplotlib.pylab as plt


def days_interval(date1, date2):
    """计算到期时间"""

    d1 = datetime.datetime.strptime(str(date1), "%Y%m%d")
    d2 = datetime.datetime.strptime(str(date2), "%Y%m%d")
    days = abs((d1 - d2).days)+1
    return float(days) /365.0


def bsmprice(S,K,sigma,T,r,q): 
    """普通期权的bsm定价公式，带股息率"""
    
    d1=(log(S/K)+(r-q+sigma**2/2)*T)/(sigma*sqrt(T))
    d2=d1-sigma*sqrt(T)

    c=S*exp(-q*T)*norm.cdf(d1)-K*exp(-r*T)*norm.cdf(d2)
    p=K*exp(-r*T)*norm.cdf(-d2)-S*exp(-q*T)*norm.cdf(-d1)

    return [c,p]


def findSx(Sx,K,r,q,v,T,PutCall):
    """找到美式期权提前行权的Sx"""

    n = 2 * (r - q) / v ** 2
    k = 2 * r / v ** 2 / (1 - exp(-r * T))
    sigma=v
    
    if Sx<0:
        y=1e1000
    elif PutCall=='C':
        q2 = (1-n+sqrt((n-1)**2+4*k))/2
        y = (bsmprice(Sx,K,sigma,T,r,q)[0]
             + (1 - exp(-q * T) * norm.cdf((log(Sx / K) + (r - q + v **2 / 2)) / v / sqrt(T))) * Sx / q2
             - Sx + K) ** 2
    elif PutCall=='P':
        q1 = (1 - n - sqrt((n - 1) ** 2 + 4 * k)) / 2
        y = (bsmprice(Sx,K,sigma,T,r,q)[1]
             - (1 - exp(-q * T) * norm.cdf(-(log(Sx / K) + (r - q + v ** 2 / 2)) / v / sqrt(T))) * Sx / q1
             + Sx - K) ** 2
    else:
        raise opttypeerr

    return y



def bawPriceCall(S,K,sigma,T,r,q):
    """美式期权baw定价近似解法 S K为当日结算价"""
    
    v=sigma
    [c,p]=bsmprice(S,K,sigma,T,r,q)
    start = S
    
    #Call价格计算
    func=lambda s:findSx(s, K, r, q, v, T, 'C')
    data = opt.fmin(func, start,disp=False)
    Sx=data[0]
   
    d1 = (log(Sx / K) + (r - q + v ** 2 / 2)) / v / sqrt(T)
    n = 2 * (r - q) / v ** 2
    k = 2 * r / v ** 2 / (1 - exp(-r * T))
    q2 = (1 - n + sqrt((n - 1) ** 2 + 4 * k)) / 2
    A2 = Sx * (1 - exp(-q * T) * norm.cdf(d1)) / q2
    if S < Sx:
        ac = c + A2 * (S / Sx) ** q2
    else:
        ac = S - K
    #print('The price of the call option is ' + str(ac))
    return ac

def bawPricePut(S,K,sigma,T,r,q):
        #Put价格计算
    
    v=sigma
    [c,p]=bsmprice(S,K,sigma,T,r,q)
    start = S
    
    func = lambda s: findSx(s, K, r, q, v, T, 'P')
    data= opt.fmin(func, start,disp=False)
    Sx=data[0]

    d1 = (log(Sx/K) + (r - q + v ** 2 / 2)) / v / sqrt(T)
    n = 2 * (r - q) / v ** 2
    k = 2 * r / v ** 2 / (1 - exp(-r * T))
    q1 = (1 - n - sqrt((n - 1) ** 2 + 4 * k)) / 2
    A1 = -Sx * (1 - exp(-q * T) * norm.cdf(-d1)) / q1
    if S > Sx:
        ap = p + A1 * (S / Sx) ** q1
    else:
        ap = K - S
    
    #print('The price of the put option is ' + str(ap))
    return ap
       


def cal_Call_Iv(iv_upper=0.55, iv_lower=0.05):
    """通过二分逼近计算看涨期权隐含波动率"""
    
    price_upper=bawPriceCall(S,K,iv_upper,T,r,q)
    price_lower=bawPriceCall(S,K,iv_lower,T,r,q)
        
    for j in range(0,100): 
        """计算中间值的iv并迭代"""
        
        iv_mid=(iv_upper+iv_lower)/2
        price_mid=bawPriceCall(S,K,iv_mid,T,r,q)    
        
        if realPrice_Call < price_mid:
            iv_upper=iv_mid
            
        else:
            iv_lower=iv_mid
                       
        iv_Call=iv_mid#以最后迭代的中间值作为最后结果
            
    return iv_Call

def cal_Put_Iv(iv_upper=0.55, iv_lower=0.05):
    """通过二分逼近计算看涨期权隐含波动率"""
    
    price_upper=bawPricePut(S,K,iv_upper,T,r,q)
    price_lower=bawPricePut(S,K,iv_lower,T,r,q)
        
    for j in range(0,100): 
        """计算中间值的iv并迭代"""
        
        iv_mid=(iv_upper+iv_lower)/2
        price_mid=bawPricePut(S,K,iv_mid,T,r,q)    
        
        if realPrice_Put < price_mid:
            iv_upper=iv_mid
            
        else:
            iv_lower=iv_mid
                       
        iv_Put=iv_mid#以最后迭代的中间值作为最后结果
            
    return iv_Put

S=2731
#K=2680#要修改
today=20220119
T=days_interval(today, 20220411)
r=0.02
q=0.02


call_workbook=xlrd.open_workbook(r"C:\Users\22977\Desktop\工作\option\data\20220119_1642661408323_Daily.xls")
call_table=call_workbook.sheet_by_name('日行情')

#计算看涨skewness
row_flag_call_start = 0
row_flag_call_end = 0

realPrice_Call_list=[]

#期权价格
for a in range(0,call_table.nrows):
    if call_table.cell(a,1).value == 'c2205-C-2540':
        row_flag_call_start = a
        break
    else:
        continue
    
for b in range(0,call_table.nrows):
    if call_table.cell(b,1).value == 'c2205-C-2840':
        row_flag_call_end = b
        break
    else:
        continue
            
for i in range(row_flag_call_start, row_flag_call_end+1):
    realPrice_Call_list.append(float(call_table.cell(i,7).value))
    
    
#写入Delta Call
delta_value_call_list=[]
delta_25_call_index=0

for c in range(row_flag_call_start, row_flag_call_end+1):
    delta_value_call_list.append(abs(0.25-float(call_table.cell(c, 10).value)))

delta_25_call_index=delta_value_call_list.index(min(delta_value_call_list))


#计算看跌skewness  
row_flag_put_start = 0
row_flag_put_end = 0

realPrice_Put_list=[]

#期权价格
for a in range(0,call_table.nrows):
    if call_table.cell(a,1).value == 'c2205-P-2540':
        row_flag_put_start = a
        break
    else:
        continue
    
for b in range(0,call_table.nrows):
    if call_table.cell(b,1).value == 'c2205-P-2840':
        row_flag_put_end = b
        break
    else:
        continue
            
for i in range(row_flag_put_start, row_flag_put_end+1):
    realPrice_Put_list.append(float(call_table.cell(i,7).value))
    
    
#写入Delta Call
delta_value_put_list=[]
delta_25_put_index=0

for c in range(row_flag_put_start, row_flag_put_end+1):
    delta_value_put_list.append(abs(0.25+float(call_table.cell(c, 10).value)))

delta_25_put_index=delta_value_put_list.index(min(delta_value_put_list))   
      
#行权价
K_list=[]

for i in range(2540,2841,20):
    K_list.append(i)
    
#波动率
realPrice_Call = realPrice_Call_list[delta_25_call_index]
K=K_list[delta_25_call_index]

iv_call_value = cal_Call_Iv(iv_upper=0.55, iv_lower=0.05)


realPrice_Put = realPrice_Put_list[delta_25_put_index]
K=K_list[delta_25_put_index]

iv_put_value = cal_Put_Iv(iv_upper=0.55, iv_lower=0.05)  
    
skewness=iv_call_value-iv_put_value

print('skewness of ' + str(today) + ' is ' + str(skewness))    
        
 
      























    
     

   