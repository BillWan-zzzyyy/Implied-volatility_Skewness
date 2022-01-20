# Implied-volatility & Skewness
## This repository is built for the purpose of getting IV of option（DCE） and its skewness.
The whole repository is based on Python.

***

## How to use this repository

The basic concept of this method is:

        1.用bs/baw算的at the money Implied vol （当天期货收盘价拿下来找到strike price离收盘价最近的那个期权）

        2.找到25 delta call和25delta put

        3.用找到的这两个call - put就是skewness

## There are several important tips about how to use files in this repository:

1. baw_call.py and baw_put.py are used to calculate the implied volatility of a series of corn options(DCE) in a specific day.
2. skewness.py is uesd to calculate skewness in a specific day.
3. If you want to see the implied volatility for a longer time period, you can then use the corn_option_call3-9.py and corn_option_put3-9.py. You can also change the parameters to get different results.





Other sources that might be helpful:

* https://github.com/dedwards25/Python_Option_Pricing
* https://github.com/khrapovs/impvol/tree/master/examples
* https://github.com/Jenniferab32/OptionAnalysis/blob/master/OptionSkew.py
* https://github.com/guiregueira/Greeks-Calculator/blob/main/Greeks_Calculator_(1)%20(1).ipynb
* https://github.com/sfl666/option_tools
