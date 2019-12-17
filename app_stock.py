#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "December 2019"


import sys
import os
import yfinance as yf
from datetime import date, timedelta
from read_tools import read_json
from flask import Flask, request, render_template, jsonify
from get_close_price import get_close_price
from get_dates import get_dates
from plot_assets import plot_assets 
from bokeh.layouts import column
from bokeh.plotting import show


app = Flask(__name__)
#
CWD = os.path.dirname(os.path.abspath(sys.argv[0]))
logfile = open(CWD + '/' + "logfile.txt",'a')
cnf = read_json('conf.json',CWD,logfile)
#
today = date.today()
tomorrow = date.today() + timedelta(days=1)
#
plot=[]
for i in cnf['assets']:
    buy_price = (i.get('buyprice'));  label = (i.get('label'))
    st_day = (i.get('buydate'));      cap_inv = (i.get('wealth'))
#
    waf = yf.Ticker(label)
    d = waf.history(start=st_day,end=tomorrow)
#
    close_price = get_close_price(d)
    dates = get_dates(d)
    p = plot_assets(label,dates,close_price)
    plot.append(p)
#
show(column(plot))
