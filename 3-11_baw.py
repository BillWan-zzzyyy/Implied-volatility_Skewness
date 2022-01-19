# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 14:36:33 2022

@author: w600178
"""


# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 16:35:26 2022

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
    #return [ac,ap]



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
            
    return round(iv_Put,5)



file_name=r"C:\Users\w600178\Desktop\Implied-volatility_Skewness-main\data\20220119_1642578147420_Daily.xls"
put_workbook=xlrd.open_workbook(file_name)
put_table=put_workbook.sheet_by_name('日行情')

S_list=[2689,2731,2730,2731]
T_list=[days_interval(20220119, 20220211),days_interval(20220119, 20220411),
   days_interval(20220119, 20220608), days_interval(20220119, 20220805),]

K_list=[]   
for d in range(2400,3001,20):
    K_list.append(d)
    
r=0.02
q=0.02    


row_flag_put_start = 0
row_flag_put_end = 0



plt.figure(figsize=(40,12))

c=0
for j in range(3,10,2):
    
    #写入期权价格
    realPrice_Put_list=[]
    for a in range(0,put_table.nrows):
        if put_table.cell(a,1).value == 'c220'+str(j)+'-P-2400':
            row_flag_put_start = a
            break
        else:
            continue
        
    for b in range(0,put_table.nrows):
        if put_table.cell(b,1).value =='c220'+str(j)+'-P-3000':
            row_flag_put_end = b
            break
        else:
            continue
                
    for i in range(row_flag_put_start, row_flag_put_end+1):
        realPrice_Put_list.append(float(put_table.cell(i,7).value))
    

        
    #写入波动率
    iv_put = []
    
    S=S_list[c]
    T=T_list[c]
    c+=1
    
        
    for i in range(0,len(K_list)):
        realPrice_Put = realPrice_Put_list[i]
        K=K_list[i]
        
        iv_put_value = cal_Put_Iv(iv_upper=0.55, iv_lower=0.05)
        iv_put.append(iv_put_value)
        
    
       
    
    #plt.figure(figsize=(30,12))
    
    color=['blue','red','yellow','green','black']
    
    plt.plot(K_list,iv_put, linewidth=3, color=color[c-1], marker='s', label='20220'+str(j))
    
    my_x_ticks = np.arange(2400, 3000, 20)
    plt.xticks(my_x_ticks)
    plt.tick_params(axis='both', which='major', labelsize=16)

    # for a, b in zip(K_list, iv_put):  # 添加这个循坏显示坐标
    #     plt.text(a, b, (a, b), ha='center', va='bottom', fontsize=10)


plt.title('20220119 strike_price vs IV 03-09 put', fontsize=24)
plt.legend()
plt.show()      
        

 























    
     

   