# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 10:36:31 2022

@author: w600178
"""


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
import xlrd



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
S=2650
K=2660  

def days_interval(date1, date2):
    d1 = datetime.datetime.strptime(str(date1), "%Y%m%d")
    d2 = datetime.datetime.strptime(str(date2), "%Y%m%d")
    days = abs((d1 - d2).days)
    return float(days) /365.0

T=days_interval(20220111,20220211)
#r=0.0521
#CNY_forward=6.4103
#CNY_spot=6.3716
r=0.02#CNY_forward/CNY_spot-1
C=26
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
#print('The Delta of closing price is '+ str(Delta(S,K,r,v,T,Type='Call')))




#画图

#当日期货收盘价20211215

#Call
S_test=2704#[2704,2748,2752,2723,2693]

#期权行权价
K_25_c=[]
for i in range(2480,3001,20):
    K_25_c.append(i)
    
#到期日
T=days_interval(20211215,20220211)
'''[days_interval(20211215, 20220212),days_interval(20211215, 20220407),
   days_interval(20211215, 20220607),days_interval(20211215, 20220805),
   days_interval(20211215, 20221014)]'''
    
#无风险利率
r=6.4103/6.3716-1


#期权价格
C_call_workbook=xlrd.open_workbook(r"C:\Users\w600178\Desktop\Implied-volatility_Skewness-main\Implied-volatility_Skewness-main\data\20211215_1641366049011_Daily.xls")

table_call=C_call_workbook.sheet_by_name('日行情')
C_call=[]
for i in range(0,len(K_25_c)):
    C_call.append(float(table_call.cell(15+i,5).value))
    


#C_call=[227,208.5,191,170.5,154,133,115.5,103.5,85.5,71.5,60,49.5,40,32.5,26,20,15,
        #12,9.5,7,5,3.5,2.5,2,1.5,1.5,1,1,0.5,0.5,0.5]

iv_call=[]

for i in range(0,len(K_25_c)):
    
    Delta25Call_v_test=impvol(S_test, K_25_c[i], T,r, C_call[i], 'C')
    
    iv_call.append(Delta25Call_v_test)
    
        
strike_price=[]    
for i in range(0,len(C_call)):
    strike_price.append(str(K_25_c[i]))
    
plt.figure(figsize=(19,6))  
plt.plot(strike_price,iv_call)
plt.title('20211215strike_price vs IV 2203 call')
plt.show()

Delta25Call=impvol(2704,2780,T,r,20,'C')


#Put
S_test=2704#[2704,2748,2752,2723,2693]

#期权行权价
K_25_p=[]
for i in range(2300,3001,20):
    K_25_p.append(i)
    
#到期日
T=days_interval(20211215,20220211)
'''[days_interval(20211215, 20220212),days_interval(20211215, 20220407),
   days_interval(20211215, 20220607),days_interval(20211215, 20220805),
   days_interval(20211215, 20221014)]'''
    
#无风险利率
r=6.4103/6.3716-1


#期权价格
C_put_workbook=xlrd.open_workbook(r"C:\Users\w600178\Desktop\Implied-volatility_Skewness-main\Implied-volatility_Skewness-main\data\20211215_1641366049011_Daily.xls")

table_put=C_put_workbook.sheet_by_name('日行情')
C_put=[]
for i in range(0,len(K_25_p)):
    C_put.append(float(table_put.cell(51+i,5).value))
    


#C_call=[227,208.5,191,170.5,154,133,115.5,103.5,85.5,71.5,60,49.5,40,32.5,26,20,15,
        #12,9.5,7,5,3.5,2.5,2,1.5,1.5,1,1,0.5,0.5,0.5]

iv_put=[]

for i in range(0,len(K_25_p)):
    
    Delta25Put_v_test=impvol(S_test, K_25_p[i], T,r, C_put[i], 'P')
    iv_put.append(Delta25Put_v_test)
    
        
strike_price=[]    
for i in range(0,len(C_put)):
    strike_price.append(str(K_25_p[i]))


plt.figure(figsize=(25,6))
#fig=px.line(x=strike_price,y=iv_put)
#fig.show()  
plt.plot(strike_price,iv_put)
plt.title('20211215strike_price vs IV 2203 put')
plt.show()
        
        
#skewness       
Delta25Call=impvol(2704,2780,T,r,20,'C')
Delta25Put=impvol(2704,2620,T,r,16,'P')      
print('IV of 25 Delta Call is '+str(Delta25Call))
print('IV of 25 Delta Put is '+str(Delta25Put))
skewness=Delta25Call-Delta25Put
print('skewness in 20211205-2203 is '+str(skewness))     
    
    







