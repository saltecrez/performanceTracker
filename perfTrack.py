#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "October 2019"


import sys
import os
import time
import yfinance as yf
from time import strftime
from datetime import datetime,timedelta,date
import pandas as pd
import PyGnuplot as pg
from readTools import readJson
 
CWD = os.path.dirname(os.path.abspath(sys.argv[0]))

logfile = open(CWD + '/' + "logfile.txt",'a')

cnf = readJson('conf.json',CWD,logfile)

en_day = date.today()

list_percent = []
list_wealth = []
for i in cnf['assets']:

    buy_price = float(i.get('buyprice'))
    label = i.get('label')
    st_day = i.get('buydate')

    list_wealth.append(i.get('wealth'))

    waf = yf.Ticker(label)
    d = waf.history(start=st_day,end=en_day)

    #------------------#
    #  closing price   #
    #------------------#
    close = d['Close']
    close_price = []
    for i in range(len(close)):
        close_price.append(close[i])

    #------------------#
    #      dates       #
    #------------------#
    dates = []
    for i in d.index:
	strip = datetime.strftime(i, '%Y-%m-%d')
	dates.append(strip)

    #------------------#
    #      percent     #
    #------------------#
    percent=[]
    for i in range(len(close_price)):
        a=float(100*(-buy_price+float(close_price[i]))/buy_price)
        percent.append(a)
    list_percent.append(percent[-1])

    #------------------#
    #      maximum     #
    #------------------#
    indmx = close_price.index(max(close_price))
    maxgain = close_price[indmx]
    maxdate = dates[indmx]
    intdy = close_price.index(close_price[-1])
    if intdy==indmx:
	print "max reached today!"

    #------------------#
    #      minimum     #
    #------------------#
    indmn = close_price.index(min(close_price))
    mingain = close_price[indmn]
    mindate = dates[indmn]
    if intdy==indmn:
	print "min reached today!"

    #------------------#
    #       plot       #
    #------------------#
    pg.s([percent])
    pg.c('set xzeroaxis linetype 3 linewidth 2.5')
    pg.c('plot "tmp.dat" w lp ')

#------------------#
#     average%     #
#------------------#
mm = float(max(list_wealth))
pesi = []
summ = 0
for i in range(len(list_wealth)):
	c = float(list_wealth[i])/mm
	pesi.append(float(list_wealth[i])/mm)
	summ = summ + list_percent[i]*c
