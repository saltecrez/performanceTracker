#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "December 2019"

def get_minimum(close_price):
    indmn = close_price.index(min(close_price))
    mingain = close_price[indmn]
    intdy = close_price.index(close_price[-1])
    if intdy==indmn:
        return True
    else: 
        return False
