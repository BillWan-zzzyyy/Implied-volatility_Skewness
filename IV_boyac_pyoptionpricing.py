# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 14:00:19 2021

@author: 22977
"""
from __future__ import division
from scipy.stats import norm
from math import *

# Cumulative normal distribution
def CND(X):
    return norm.cdf(X)

# Black Sholes Function
def BlackScholes(CallPutFlag,S,K,t,r,s):
    """
    S = Current stock price
    t = Time until option exercise (years to maturity)
    K = Option striking price
    r = Risk-free interest rate   此处需要修改为CNYforward/CNYspot -1
    N = Cumulative standard normal distribution
    e = Exponential term
    s = St. Deviation (volatility)
    Ln = NaturalLog
    """
    d1 = (log(S/K) + (r + (s ** 2)/2) * t)/(s * sqrt(t))
    d2 = d1 - s * sqrt(t)

    if CallPutFlag=='c':
        return S * CND(d1) - K * exp(-r * t) * CND(d2) # call option
    else:
        return K * exp(-r * t) * CND(-d2) - S * CND(-d1) # put option 


if __name__ == "__main__":
    # Number taken from: http://wiki.mbalib.com/wiki/Black-Scholes
    print('Option_price='+str(BlackScholes('c', S=164.0, K=165.0, t=0.0959, r=0.0521,s=0.29))) # 5.788529972549341
