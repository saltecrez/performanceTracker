#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "December 2019"

import time
import numpy as np
from bokeh.plotting import figure
from bokeh.plotting import output_file
from bokeh.models import HoverTool
from bokeh.models import DatetimeTickFormatter
from bokeh.models import Title
from bokeh.models import Span
from bokeh.models import CrosshairTool 
from datetime import datetime as dt


def plot_assets(label,x,y,z):
    window_size = 30
    window = np.ones(window_size)/float(window_size)
    TOOLS = 'box_zoom,box_select,crosshair,reset'
    output_file("stocks.html", title="Performance tracker")
    p = figure(plot_width=800, plot_height=350, tools=TOOLS, toolbar_location=None)
    p.line(x, y, line_width=2, line_color="greenyellow") 
    # Title
    p.add_layout(Title(text=str(y[-1]), text_font_style="bold", text_font_size="13pt", text_font='Cantarell'), 'above')
    p.add_layout(Title(text=label, text_font_style="bold", text_font_size="16pt", text_font='Cantarell'), 'above')
    # Axes
    p.xaxis.minor_tick_line_color = None
    p.yaxis.minor_tick_line_color = None
    p.xaxis.ticker.desired_num_ticks = 7
    p.xaxis.major_label_text_font_size = "11pt"
    p.xaxis.major_label_text_font = "Cantarell"
    p.xaxis.major_label_text_font_style = "bold"
    p.yaxis.major_label_text_font_size = "11pt"
    p.yaxis.major_label_text_font = "Cantarell"
    p.yaxis.major_label_text_font_style = "bold"
    p.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d-%m-%Y"],
        days=["%d-%m-%Y"],
        months=["%d-%m-%Y"],
        years=["%d-%m-%Y"],
    )
    # Grid
    p.grid.grid_line_color = 'gray'
    p.grid.grid_line_alpha = 0.5
    # Background
    p.background_fill_color = "black"
    # Horizontal line
    hline = Span(location=z, dimension='width', line_color='red', line_width=3)
    p.renderers.extend([hline])
    # Tools: hover and crosshair
    p.add_tools(CrosshairTool(line_color="red"))
    p.add_tools(HoverTool(
    tooltips=[
        ( 'date',   '@x{%F}'            ),
        ( 'price',  '@{y}{%0.2f}' ),
        ("canvas (x,y)", "(0, 0)")
    ],
    formatters={
        'x'      : 'datetime',
        'y' : 'printf',
    },
    mode='vline'
    ))
    return p
