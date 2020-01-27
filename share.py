#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "January 2020"

import yfinance as yf
from datetime import date
from datetime import timedelta

class HistoricalData(object):
    def __init__(self, label, buy_date):
        self.label = label
        self.buy_date = buy_date
        self.tomorrow = date.today() + timedelta(days=1)

    def get_historical_data(self):
        locator = yf.Ticker(self.label)
        hd = locator.history(start=self.buy_date,end=self.tomorrow)
        return hd

class Share(HistoricalData):
    def __init__(self, label, buy_date, buy_price):
        self.buy_price = buy_price
        HistoricalData.__init__(self, label, buy_date)
        self.d = HistoricalData.get_historical_data(self)

    def get_close_price(self):
        close = self.d['Close']
        close_price = [close[i] for i in range(len(close))]
        return close_price

    def get_dates(self):
        dates = [i for i in self.d.index]
        return dates

x = Share("AFX.DE","2019-10-23","93.123")
print(x.get_dates())
