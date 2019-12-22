#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "December 2019"

def get_maximum(close_price):
    indmx = close_price.index(max(close_price))
    maxgain = close_price[indmx]
    intdy = close_price.index(close_price[-1])
    if intdy==indmx:
        return True
    else:
        return False
