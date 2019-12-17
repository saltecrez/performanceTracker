#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "December 2019"

def get_close_price(d):
    close = d['Close']
    close_price = []
    for i in range(len(close)):
        close_price.append(close[i])
    return close_price
