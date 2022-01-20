# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 14:31:50 2021

@author: 22977
"""
from math import exp, log, sqrt, erf
import numpy as np
import matplotlib.pylab as plt
from scipy.stats import norm
import datetime


##Step 1: calculate the implied volatility using B-S Formula

#setting parametres:
#source:DCE crawler(Dalian_Option-Crawler)
''' 
S - stock price
K - strike price
T - maturity in years(/242)
r - risk free rate annualized 
C - option price
cp - call/put flag
sig: volatililty annualized
'''

#目前取得是3月期权的数 还未更新为1月的



#initialize parametres using data from DCE
S=2693
K=2700
T=34/242
#r=0.0521
CNY_forward=6.4152
CNY_spot=6.3651
r=CNY_forward/CNY_spot-1
C=41.5
cp ='C'

# Standard Normal distribution with math library only
def Phi(x):
    return .5 * ( 1. + erf(x / sqrt(2)) )  


#B-S Formula

def BS(S, K, T, r, sig, cp):
    d1 = (log(S/K) + r*T) / (sig*sqrt(T)) + .5 * sig*sqrt(T)
    d2 = d1 - sig*sqrt(T)
    value = 0
    if cp == 'C':
        value = S*Phi(d1) - K*exp(-r*T)*Phi(d2)
    if cp == 'P':
        value = K*exp(-r*T)*Phi(-d2) - S*Phi(-d1)
    return value

# Function to find BS Implied Vol using Bisection Method
#tol: tolerance
#calculate volatility based on B-S Formula

def impvol(S, K, T, r, C, cp, tol = 1e-5, fcount = 1e4):
    sig, sig_u, sig_d = .2, 1., 1e-3
    count = 0
    err = BS(S, K, T, r, sig, cp) - C

    # repeat until error is sufficiently small or counter hits fcount
    while abs(err) > tol and count < fcount:
        if err < 0:
            sig_d = sig
            sig = (sig_u + sig)/2
        else:
            sig_u = sig
            sig = (sig_d + sig)/2
        
        err = BS(S, K, T, r, sig, cp) - C
        count += 1
    
    # return NA if counter hit fcount
    if count == fcount:
        return -1
    else:
        return sig
        
    
    #this sig is the implied volatility we want


#Test code:
#S, K, T, r, C, cp = 164., 165., 23./242, 0.0521, 5.78, 'C'

#At the money implied volatility
#v: implied volatility
v = impvol(S, K, T, r, C, cp)
print('At the money Implied volatility: %.4f' % v)




##Step 2: calculate the Delta using implied volatility and B-S Formula

def Delta(S, K, r, v, T,Type="Call"):
  #variation of option price per unit of variation of stock price
  #d1=D1(S,K,r,v,T)
  d1 = (log(S/K) + r*T) / (v*sqrt(T)) + .5 * v*sqrt(T)
  if Type=="Call":
    myDelta=norm.cdf(d1)
  else:
    myDelta=norm.cdf(d1)-1
  return myDelta

#call:Type='Call' put: Type='Put'
print('The Delta of closing price is '+ str(Delta(S,K,r,v,T,Type='Call')))



##Step 3: Skewness


#initialize parametres using data from DCE
#计算剩余期限
def days_interval(date1, date2):
    d1 = datetime.datetime.strptime(str(date1), "%Y%m%d")
    d2 = datetime.datetime.strptime(str(date2), "%Y%m%d")
    days = abs((d1 - d2).days)
    return float(days) /365.0

#date2是交割月份前一个月的第五个交易日
    
#25 Delta Call
S=2693
K_25c=2780
T=days_interval(20211217,20220212)#以202203到期期权为例
r=CNY_forward/CNY_spot-1
C_call=15
cp ='C'

Delta25Call_v=impvol(2693, K_25c, T, 0.00787, C_call, 'C')
print('25 Delta Call Implied volatility: %.4f' % Delta25Call_v)


#25 Delta Put
S=2693
K_25p=2620
T=days_interval(20211217,20220212)
r=CNY_forward/CNY_spot-1
C_put=16.5
cp ='P'

Delta25Put_v=impvol(2693, K_25p, T, 0.00787, C_put, 'P')
print('25 Delta Put Implied volatility: %.4f' % Delta25Put_v)


#Skewness
Skewness=Delta25Call_v-Delta25Put_v
print('Skewness='+ str(Skewness))



#test code for 0823-0901
#数据源为3月到期 还未修改

#25 Delta Call

S_test=[2550,2527,2521,2516,2496,2503,2507,2483]

K_25_c=[2680,2700,2700,2680,2660,2660,2660,2640]
K_25_p=[2380,2380,2380,2380,2380,2380,2380,2360]
T=[days_interval(20210823, 20220212),days_interval(20210824, 20220212),
   days_interval(20210825, 20220212),days_interval(20210826, 20220212),
   days_interval(20210827, 20220212),days_interval(20210830,20220212),
   days_interval(20210831, 20220212),days_interval(20210901, 20220212)]

r=6.5/6.39-1
C_call=[36,36.5,30,32,33.5,33.5,34,30]
C_put=[36,32,31.5,32,30,34.5,30,26.5]
test_skewness_picture=[]
iv_call25=[]
iv_put25=[]
for i in range(0,8):
    
    Delta25Call_v_test=impvol(S_test[i], K_25_c[i], T[i],r, C_call[i], 'C')
    Delta25Put_v_test=impvol(S_test[i], K_25_p[i], T[i],r, C_put[i], 'P')
    
    iv_call25.append(Delta25Call_v_test)
    iv_put25.append(Delta25Put_v_test)
    
    skewness_test=Delta25Call_v_test-Delta25Put_v_test
    test_skewness_picture.append(skewness_test)
    
date=['0823','0824','0825','0826','0827','0830','0831','0901']
plt.subplot(3,1,1)
plt.plot(date,test_skewness_picture)
plt.title('Skewness vs date')
plt.show()

plt.subplot(312)
plt.plot(date,iv_call25)
plt.title('Delta25 Implied volatility of Call')
plt.show()

plt.subplot(313)
plt.title('Delta25 Implied volatility of Put')
plt.plot(date,iv_put25)
plt.show()

        
        
       
        
    
    

'''Delta25Call_v=impvol(2693, K_25c, T, 0.00787, C_call, 'C')
print('25 Delta Call Implied volatility: %.4f' % Delta25Call_v)




print('25 Delta Put Implied volatility: %.4f' % Delta25Put_v)


#Skewness
Skewness=Delta25Call_v-Delta25Put_v
print('Skewness='+ str(Skewness))'''





