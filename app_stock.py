#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "December 2019"


import sys
import os
import yfinance as yf
import numpy as np
from datetime import date, timedelta
from flask import Flask, request, render_template, jsonify
from read_tools import read_json
from get_close_price import get_close_price
from get_dates import get_dates
from plot_assets import plot_assets
from percent_calculator import percent_calculator
from weighted_mean import weighted_mean
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
total_wealth_array = []
latest_gain_loss = []
for i in cnf['assets']:
    buy_price = float((i.get('buyprice')));  label = (i.get('label'))
    st_day = (i.get('buydate'));      cap_inv = float((i.get('wealth')))
#
    waf = yf.Ticker(label)
    d = waf.history(start=st_day,end=tomorrow)
#
    total_wealth_array.append(cap_inv)
    close_price = get_close_price(d)
    dates = get_dates(d)
    gain_loss = percent_calculator(close_price,buy_price)
    latest_gain_loss.append(gain_loss[-1])
    p = plot_assets(label,dates,close_price,buy_price)
    plot.append(p)
#
total_yield = round(weighted_mean(total_wealth_array,latest_gain_loss),3)
total_wealth = np.sum(total_wealth_array)
