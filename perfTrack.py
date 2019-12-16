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
import numpy as np
import PyGnuplot as pg
from readTools import readJson
from percentCalculator import percentCalculator

CWD = os.path.dirname(os.path.abspath(sys.argv[0]))
logfile = open(CWD + '/' + "logfile.txt",'a')
cnf = readJson('conf.json',CWD,logfile)
today = date.today()
tomorrow = date.today() + timedelta(days=1)

list_percent = []

mul_cap = []
mul_pri = []
mul_lab = []
mul_dat = []

pg.c('set multiplot layout 4, 3 title "Multiplot layout 4, 3" font ",14"')

for i in cnf['activemultipleassets']:

    buy_price = float(i.get('buyprice'))
    labelmul     = i.get('label')
    st_daymul    = i.get('buydate')
    capi_inv   = i.get('wealth')

    mul_cap.append(capi_inv)
    mul_pri.append(buy_price)
    mul_lab.append(labelmul)
    mul_dat.append(st_daymul)

# Find indexes
index = []
unique = list(set(mul_lab))
mama=[]
papa=[]
for label in unique:
    par_cap=[]
    par_pri=[]
    par_dat=[]
    indices = [i for i, x in enumerate(mul_lab) if x == label]
    for j in indices:
        par_cap.append(mul_cap[j])
        par_pri.append(mul_pri[j])
        par_dat.append(mul_dat[j])
    coeff = float(min(par_cap))/float(max(par_cap))
    ind_max_cap = par_cap.index(max(par_cap))
    ind_min_cap = par_cap.index(min(par_cap))
    average_price=((float(par_pri[ind_max_cap])*1.0+float(par_pri[ind_min_cap])*coeff)/(1.0+coeff))
    total_capital=(float(min(par_cap))+float(max(par_cap)))
    mama.append(total_capital)

    waf = yf.Ticker(label)
    d = waf.history(start=par_dat[0],end=tomorrow)
    close = d['Close']
    close_price = []
    for i in range(len(close)):
        close_price.append(close[i])
    dates = []
    for i in d.index:
        strip = datetime.strftime(i, '%Y-%m-%d')
        dates.append(strip)
    percent = percentCalculator(close_price,average_price)
    list_percent.append(percent[-1])
    indmx = close_price.index(max(close_price))
    maxgain = close_price[indmx]
    maxdate = dates[indmx]
    intdy = close_price.index(close_price[-1])
    if intdy==indmx:
        msg = label + ' has reached a new maximum: ' + str(round(percent[-1],2)) + "%"
        print msg
        bashCommand= "(echo 'Subject: '"+label+"; echo; echo '" + msg + "') | /usr/sbin/sendmail -i elisa.londero@inaf.it"
        os.system(bashCommand)
    indmn = close_price.index(min(close_price))
    mingain = close_price[indmn]
    mindate = dates[indmn]
    if intdy==indmn:
        msg = label + ' has reached a new minimum: ' + str(round(percent[-1],2)) + "%"
        print msg
        bashCommand= "(echo 'Subject: '"+label+"; echo; echo '" + msg + "') | /usr/sbin/sendmail -i elisa.londero@inaf.it"
        os.system(bashCommand)

    #------------------#
    #      output      #
    #------------------#
    print "#------------------#"
    print "#      "+label
    print "#------------------#"
    print "rendimento: " + str(round(percent[-1],2)) + "%"
    print "capitale  : " + str(total_capital) + " EUR"
    print "\n"

list_wealth=[]
for i in cnf['activeassets']:

    label     = i.get('label')
    st_day    = i.get('buydate')
    buy_price = float(i.get('buyprice'))
    cap_inv   = i.get('wealth')
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
    percent = percentCalculator(close_price,buy_price)
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
total_wealth =  list_wealth + mama
mm = float(max(total_wealth))
weigths = []
summ = 0
tot_wealth = 0.0
for i in range(len(total_wealth)):
	c = float(total_wealth[i])/mm
	tot_wealth = tot_wealth + float(total_wealth[i])
	weigths.append(float(total_wealth[i])/mm)
	summ = summ + list_percent[i]*c
tot = summ/sum(weigths)

print "#-------------------#"
print "# Rendimento totale #"
print "#-------------------#"
print "rendimento tot: " + str(round(tot,2)) + "%"
print "capitale tot  : " + str(tot_wealth) + " EUR"
print "\n"

for i in cnf['soldassets']:

    sell_price = float(i.get('sellprice'))
    label = i.get('label')
    sell_day = i.get('selldate')

    waf = yf.Ticker(label)
    d = waf.history(start=st_day,end=tomorrow)

    close = d['Close']
    close_price = []
    for i in range(len(close)):
        close_price.append(close[i])

    last_price = close_price[-1]

    delta = last_price - sell_price
    if delta < 0.0:
	percent_drop = delta*100/sell_price
        print percent_drop
        print "#------------------#"
        print "#      sold stuff"
        print "#------------------#"
	print label, ' dropped by ' + str(round(percent_drop,2)) + '% since you sold it'
        msg = label + ' dropped by ' + str(round(percent_drop,2)) + '% since you sold it'
        bashCommand= "(echo 'Subject: '"+label+"; echo; echo '" + msg + "') | /usr/sbin/sendmail -i elisa.londero@inaf.it"
        os.system(bashCommand)

for j in cnf['keepaneyeon']:
    label = j.get('label')
    waf = yf.Ticker(label)
    st_day = "2019-10-01"
    d = waf.history(start=st_day,end=tomorrow)

    close = d['Close']
    close_price = []
    for i in range(len(close)):
        close_price.append(close[i])

    dates = []
    for i in d.index:
        strip = datetime.strftime(i, '%Y-%m-%d')
        dates.append(strip)

    # algoritmo
    trial = close_price[::-1]
    dateback = dates[::-1]
    loss = []
    lossprice=[]
    for i in range(len(trial)):
        if i==0:
            trial[i-1]=close_price[-1]
        dum = trial[i-1]-trial[i]
        if dum>0.1:
            break
        else:
            loss.append(dum)
            lossprice.append(trial[i])
    perclost =  (max(lossprice)-close_price[-1])/close_price[-1]*100
    if perclost>0.0:
        print label, 'lost ',  str(round(perclost,2))   , '% in ', len(loss), 'days'
