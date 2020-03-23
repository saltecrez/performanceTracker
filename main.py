#!/usr/bin/env python
  
__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "February 2020"

from share import Share
from flask import Flask
from json_parser import SharesJsonParser
from utilities import VerifyLinux
from json_parser import SharesJsonParser
from plot_assets import PlotAssets
from bokeh.layouts import column
from bokeh.plotting import show
from portfolio import Portfolio
from portfolio import SortOutShares

rj = SharesJsonParser()

def main():
    VerifyLinux()
    app = Flask(__name__)
    shares_list = rj._get_shares()
    sos = SortOutShares()
    pf = Portfolio()
    labels = sos.find_all_labels()
    ml = sos.find_multiple_labels()
    sl = sos.find_single_labels()
    plot=[]

    for label in ml:

        i = sos.join_shares(label)
        sh = Share(label,i[0],i[1],i[2]) 
        share_yield = sh.get_yield()
        dates = sh.get_dates()
        clprice = sh.get_close_price()
        loss = sh.fall_from_max()
        pa = PlotAssets(label,dates,clprice,float(i[1]),share_yield,loss).plot_assets()
        plot.append(pa)

    for label in sl:

        i = sos.select_single_shares(label)
        sh = Share(label,i[0],i[1],i[2])
        share_yield = sh.get_yield()
        dates = sh.get_dates()
        clprice = sh.get_close_price()
        loss = sh.fall_from_max()
        pa = PlotAssets(label,dates,clprice,float(i[1]),share_yield,loss).plot_assets()
        plot.append(pa)

    show(column(plot))

if __name__ == "__main__":
    main()
