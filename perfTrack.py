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
from createDate import createDate
 
CWD = os.path.dirname(os.path.abspath(sys.argv[0]))

logfile = open(CWD + '/' + "logfile.txt",'a')

cnf = readJson('conf_elisa.json',CWD,logfile)
#cnf = readJson('conf_carlo.json',CWD,logfile)

#en_day = date.today()
tomorrow = date.today() + timedelta(days=1)

list_percent = []
list_wealth = []

pg.c('set multiplot layout 4, 3 title "Multiplot layout 4, 3" font ",14"')

for i in cnf['assets']:

    buy_price = float(i.get('buyprice'))
    label = i.get('label')
    st_day = i.get('buydate')

    cap_inv = i.get('wealth')
    list_wealth.append(cap_inv)

    waf = yf.Ticker(label)
    d = waf.history(start=st_day,end=tomorrow)

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
	msg = label + ' has reached a new maximum: ' + str(round(percent[-1],2)) + "%"
	bashCommand= "(echo 'Subject: '"+label+"; echo; echo '" + msg + "') | /usr/sbin/sendmail -i elisa.londero@inaf.it"
	os.system(bashCommand)

    #------------------#
    #      minimum     #
    #------------------#
    indmn = close_price.index(min(close_price))
    mingain = close_price[indmn]
    mindate = dates[indmn]
    if intdy==indmn:
	msg = label + ' has reached a new minimum: ' + str(round(percent[-1],2)) + "%"
	bashCommand= "(echo 'Subject: '"+label+"; echo; echo '" + msg + "') | /usr/sbin/sendmail -i elisa.londero@inaf.it"
	os.system(bashCommand)

    #------------------#
    #       plot       #
    #------------------#
    pg.s([percent],filename=label+'.dat')
    pg.c('set xzeroaxis linetype 3 linewidth 2.5')
    pg.c('plot "' + label + '.dat" w lp ')

    #------------------#
    #      output      #
    #------------------#

    print "#------------------#"
    print "#      "+label
    print "#------------------#"
    print "rendimento: " + str(round(percent[-1],2)) + "%"  
    print "capitale  : " + str(cap_inv) + " EUR" 
    print "\n"

#------------------#
#     average%     #
#------------------#
mm = float(max(list_wealth))
pesi = []
summ = 0
patrimonio=0.0
for i in range(len(list_wealth)):
	c = float(list_wealth[i])/mm
	patrimonio = patrimonio + float(list_wealth[i])
	pesi.append(float(list_wealth[i])/mm)
	summ = summ + list_percent[i]*c
tot= summ/sum(pesi)

print "#------------------#"
print "rendimento tot: " + str(round(tot,2)) + "%"
print "capitale tot  : " + str(patrimonio) + " EUR"
print "\n"
