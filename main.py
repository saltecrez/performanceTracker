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

rj = SharesJsonParser()

def main():
    VerifyLinux()
    app = Flask(__name__)
    shares_list = rj._get_shares()
    plot=[]
    for i in shares_list:
        sh = Share(i[0],i[1],i[2],i[3])
        dates = sh.get_dates()
        clprice = sh.get_close_price()
        pa = PlotAssets(i[0],dates,clprice,float(i[2])).plot_assets()
        plot.append(pa)

    show(column(plot))


if __name__ == "__main__":
    main()
