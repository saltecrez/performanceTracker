#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "January 2020"

import yfinance as yf
from datetime import date
from datetime import timedelta

class Share(object):
    def __init__(self, label, buy_date, buy_price, wealth):
        self.label = label
        self.wealth = wealth
        self.buy_date = buy_date
        self.buy_price = buy_price
        self.tomorrow = date.today() + timedelta(days=1)

    def _get_historical_data(self):
        locator = yf.Ticker(self.label)
        hd = locator.history(start=self.buy_date,end=self.tomorrow)
        return hd

    def get_close_price(self):
        close = self._get_historical_data()['Close'] 
        close_price = [close[i] for i in range(len(close))]
        return close_price

    def get_dates(self):
        dates = [i for i in self._get_historical_data().index]
        return dates

    def test_if_last_maximum(self):
        indmx = self.get_close_price().index(max(self.get_close_price()))
        inlst = self.get_close_price().index(self.get_close_price()[-1])
        if inlst == indmx:
            return True
        else:
            return False

    def test_if_last_minimum(self):
        indmn = self.get_close_price().index(min(self.get_close_price()))
        inlst = self.get_close_price().index(self.get_close_price()[-1])
        if inlst == indmn:
            return True
        else:
            return False

    def get_percent(self):
        percent = []
        cp = self.get_close_price()
        for i in range(len(cp)):
            delta = float(cp[i])-float(self.buy_price)
            dummy = 100*delta/float(self.buy_price)
            percent.append(dummy)
        return percent

    def get_yield(self):
        percent = self.get_percent()
        latest_yield_rounded = round(percent[-1],3)
        return latest_yield_rounded

    def fall_from_max(self):
        indmx = self.get_close_price().index(max(self.get_close_price()))
        maxperc = self.get_percent()[indmx]
        lastperc = self.get_percent()[-1]
        loss = lastperc-maxperc
        if loss < 0:
            return round(loss,2) 

if __name__ == "__main__":
    sh = Share('AFX.DE','2019-10-23','93.123','5005.8')
    print(sh.get_close_price())
    print(sh.get_percent())
