# Implied-volatility_Skewness
## This repository is built for the purpose of getting IV and its skewness.
The whole repository is based on Python.

***
Some useful link that I used to build this repository:

* https://github.com/boyac/pyOptionPricing.git    This one is for the calculation of IV
* https://github.com/pfmoro/Black-Scholes-Greeks/blob/master/BSG.py    This one is for the calculation of Delta 

Data source:

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
