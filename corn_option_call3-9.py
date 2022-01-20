# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 16:18:15 2022

@author: 22977
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 14:38:57 2022

@author: 22977
"""
"""计算202203-09到期的玉米看多期权的隐含波动率并画图"""

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
            
    return round(iv_Call,5)



    
    
#以下三个参数需要根据情况修改
#文件名
file_name=r"C:\Users\22977\Desktop\工作\option\data\20220119_1642661408323_Daily.xls"
call_workbook=xlrd.open_workbook(file_name)
call_table=call_workbook.sheet_by_name('日行情')

#四个月对应的当日期货价格
S_list=[2689,2731,2730,2731]

#到期日期
day=20220119

T_list=[days_interval(day, 20220211),days_interval(day, 20220411),
   days_interval(day, 20220608), days_interval(day, 20220805),]

#行权价
K_list=[]   
for d in range(2400,3001,20):
    K_list.append(d)
    
r=0.02
q=0.02    

row_flag_call_start = 0
row_flag_call_end = 0


#循环画出每个月的iv曲线
plt.figure(figsize=(50,12))

c=0 #控制S和T
for j in range(3,10,2):
    
    #写入期权价格
    realPrice_Call_list=[]
    for a in range(0,call_table.nrows):
        if call_table.cell(a,1).value == 'c220'+str(j)+'-C-2400':
            row_flag_call_start = a
            break
        else:
            continue
        
    for b in range(0,call_table.nrows):
        if call_table.cell(b,1).value =='c220'+str(j)+'-C-3000':
            row_flag_call_end = b
            break
        else:
            continue
                
    for i in range(row_flag_call_start, row_flag_call_end+1):
        realPrice_Call_list.append(float(call_table.cell(i,7).value))
    

        
    #写入波动率
    iv_call = []
    
    S=S_list[c]
    T=T_list[c]
    c+=1
    
        
    for i in range(0,len(K_list)):
        realPrice_Call = realPrice_Call_list[i]
        K=K_list[i]
        
        iv_call_value = cal_Call_Iv(iv_upper=0.55, iv_lower=0.05)
        iv_call.append(iv_call_value)
        
    
    #画图
    color=['blue','red','yellow','green','black']
    
    plt.plot(K_list,iv_call, linewidth=3, color=color[c-1], marker='s', label='20220'+str(j))
    
    my_x_ticks = np.arange(2400, 3020, 40)
    plt.xticks(my_x_ticks)
    plt.tick_params(axis='both', which='major', labelsize=16)

    # for a, b in zip(K_list, iv_put):  # 添加这个循坏显示坐标
    #     plt.text(a, b, (a, b), ha='center', va='bottom', fontsize=10)



plt.title(str(day) + 'Strike_price vs IV 202203-09 Call', fontsize=24)
plt.legend()
plt.show()      
     

 























    
     

   