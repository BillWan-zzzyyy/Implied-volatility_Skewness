# Implied-volatility & Skewness
## This repository is built for the purpose of getting IV of option and its skewness.
The whole repository is based on Python.

***

## How to use this repository

The basic concept of this method is:

        1.用bs算的at the money Implied vol （当天期货收盘价拿下来找到strike price离收盘价最近的那个期权）

        2.用bs算出每天期权收盘价的delta

        3.找到25 delta call和25delta put

        4.用第3步中找到的这两个call - put就是skewness

## There are several important tips about the files in this repository:

1. The primary file of this repository is get_IV_by_BS. You can run this python file to get the implied volatility, the value of Delta and skewness of a certain option.
2. The data source which I used to get the information of options is the website of DCE. To get all the information automatically, I use the Python file Dalian_Option_Crawler. This crawler is the work of yuany3721. You can find the link of his original repository in the below links.
3. Besides these two files, other files such as Greek_pfmoro are just for the purpose of displaying other methods to build B-S Formulas or calculate Greeks. I also uploaded another crawler which is designed to get details of SSE50.
4. To sum up, you should first use the Dalian_Option_Crawler to get the data. Then you change the parameters in get_IV_by_BS to calculate the implied volatility and skewness. You may realize that this method does not develop automatic way to update parameters. I will try to optimize this feature asap.


***
# Some useful link that I used to build this repository:

* https://github.com/boyac/pyOptionPricing.git    This one is for the calculation of IV
* https://github.com/pfmoro/Black-Scholes-Greeks/blob/master/BSG.py    This one is for the calculation of Delta
* https://github.com/casprwang/sse-option-crawler  This is the crawler to get information of DCE.

Some other Data source you might think helpful:

    1. Realtime quote data obtained from CBOE.
    
    Update global variable g_csvfile in OptionSkew.py with the name of the file downloaded from CBOE that contains the option chain.
    
    http://www.cboe.com/delayedquote/quote-table-download
    
    2. A crawler for SSE50 Index Option
    
    https://github.com/casprwang/sse-option-crawler.git

Other sources that might be helpful:

* https://github.com/dedwards25/Python_Option_Pricing
* https://github.com/khrapovs/impvol/tree/master/examples
* https://github.com/Jenniferab32/OptionAnalysis/blob/master/OptionSkew.py
* https://github.com/guiregueira/Greeks-Calculator/blob/main/Greeks_Calculator_(1)%20(1).ipynb
* https://github.com/sfl666/option_tools
