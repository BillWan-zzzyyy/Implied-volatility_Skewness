# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 14:31:50 2021

@author: 22977
"""
from math import exp, log, sqrt, erf
import numpy as np
import matplotlib.pylab as plt
from scipy.stats import norm


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


#v: implied volatility
v = impvol(S, K, T, r, C, cp)
print('Implied volatility: %.4f' % v)




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
print(Delta(S,K,r,v,T,Type='Call'))



##Step 3: Skewness


#initialize parametres using data from DCE
#25 Delta Call
S=2693
K=2780
T=34/242
r=CNY_forward/CNY_spot-1
C=15
cp ='C'

Delta25Call_v=impvol(2693, 2780, 34/242, 0.00787, 15, 'C')
print('25 Delta Call Implied volatility: %.4f' % Delta25Call_v)


#25 Delta Put
S=2693
K=2620
T=34/242
r=CNY_forward/CNY_spot-1
C=16.5
cp ='P'

Delta25Put_v=impvol(2693, 2620, 34/242, 0.00787, 16.5, 'P')
print('25 Delta Put Implied volatility: %.4f' % Delta25Put_v)


#Skewness
Skewness=Delta25Call_v-Delta25Put_v
print('Skewness='+ str(Skewness))







