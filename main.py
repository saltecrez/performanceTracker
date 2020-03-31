#!/usr/bin/env python
  
__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "February 2020"

from share import Share
from flask import Flask
from flask import Markup
from flask import request
from bokeh.embed import file_html
from bokeh.embed import components
from flask import render_template
from bokeh.resources import CDN
from json_parser import SharesJsonParser
from utilities import VerifyLinux
from json_parser import SharesJsonParser
from plot_assets import PlotAssets
from bokeh.layouts import column
from bokeh.plotting import show
from portfolio import Portfolio
from portfolio import SortOutShares

app = Flask(__name__)
rj = SharesJsonParser()

@app.route('/', methods=['POST', 'GET'])
def index():
    VerifyLinux()
    shares_list = rj._get_shares()
    sos = SortOutShares()
    pf = Portfolio()
    labels = sos.find_all_labels()
    ml = sos.find_multiple_labels()
    sl = sos.find_single_labels()
    plot = []; ps = []; div = []; lab = []; sy = []; cp = []; ffm = [];

    for label in ml:

        i = sos.join_shares(label)
        sh = Share(label,i[0],i[1],i[2]) 
        share_yield = sh.get_yield()
        dates = sh.get_dates()
        clprice = sh.get_close_price()
        loss = sh.fall_from_max()
        pa = PlotAssets(label,dates,clprice,float(i[1]),share_yield,loss).plot_assets()
        plot_script, plot_div = components(pa)
        ps.append(plot_script)
        div.append(plot_div)
        lab.append(label)
        sy.append(share_yield)
        cp.append(clprice[-1])
        ffm.append(loss)

    for label in sl:

        i = sos.select_single_shares(label)
        sh = Share(label,i[0],i[1],i[2])
        share_yield = sh.get_yield()
        dates = sh.get_dates()
        clprice = sh.get_close_price()
        loss = sh.fall_from_max()
        pa = PlotAssets(label,dates,clprice,float(i[1]),share_yield,loss).plot_assets()
        plot_script, plot_div = components(pa)
        ps.append(plot_script)
        div.append(plot_div)
        lab.append(label)
        sy.append(share_yield)
        cp.append(clprice[-1])
        ffm.append(loss)

    dic_list = []
    kwargs = {}
    if request.method == 'GET':
        for j in range(len(ps)):
            kwargs = {'plot_script': ps[j], 'plot_div': div[j], 'labels': lab[j], 'yield': sy[j], 'closeprice': cp[j], 'fallfrommax': ffm[j]}
            dic_list.append(kwargs)
        return render_template('index.html', dic_list = dic_list)
    abort(404)
    abort(Response('Hello'))

if __name__ == "__main__":
    app.run(debug=True)
