#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "January 2020"

import yfinance as yf
from datetime import date
from datetime import timedelta

class Share:
    def __init__(self, label, buy_price, buy_date, wealth):
        self.label = label
        self.buy_price = buy_price
        self.buy_date = buy_date
        self.wealth = wealth
        self.tomorrow = date.today() + timedelta(days=1)

    def get_historical_data(self):
        locator = yf.Ticker(self.label)
        hd = locator.history(start=self.buy_date,end=self.tomorrow)
        return hd

if __name__ == "__main__":
    Share("AFX.DE","93.123","2019-10-23","5005.8").get_historical_data()
