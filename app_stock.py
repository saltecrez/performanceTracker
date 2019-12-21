#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "December 2019"


import sys
import os
import yfinance as yf
import numpy as np
from datetime import date
from datetime import timedelta
from datetime import datetime
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
latest_gain_array = []
#
for i in cnf['assets']:
#
    label = (i.get('label')); multiple_asset = (i.get('multiple'))
#
    if multiple_asset == "y":
        cap_inv_array = []
        buy_date_array = []
        buy_price_array = []
        date_format = '%Y-%m-%d'

        for k in i.get('nested'):
            single_buy_price = float(k.get('buyprice'));
            single_buy_date = (k.get('buydate'));
            single_cap_inv = float((k.get('wealth')))

            cap_inv_array.append(single_cap_inv)
            buy_date_array.append(datetime.strptime(single_buy_date,date_format))
            buy_price_array.append(single_buy_price)

        cap_inv = np.sum(cap_inv_array)
        buy_date = min(buy_date_array)
        buy_price = weighted_mean(cap_inv_array,buy_price_array)

    elif multiple_asset == "n":
        buy_price = float((i.get('buyprice')));
        buy_date = (i.get('buydate')); cap_inv = float((i.get('wealth')))
#
    waf = yf.Ticker(label)
    d = waf.history(start=buy_date,end=tomorrow)
#
    total_wealth_array.append(cap_inv)
    close_price = get_close_price(d)
    dates = get_dates(d)
    gain_loss = percent_calculator(close_price,buy_price)
    latest_gain_array.append(gain_loss[-1])
    p = plot_assets(label,dates,close_price,buy_price,round(gain_loss[-1],3))
    plot.append(p)
#
total_yield = round(weighted_mean(total_wealth_array,latest_gain_array),3)
total_wealth = np.sum(total_wealth_array)
show(column(plot))
