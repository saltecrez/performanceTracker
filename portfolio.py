#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "February 2020"


class Portfolio(object):
    def __init__(self):
        self.shares = []

    def add_share(self):
        self.shares.append(Share(label, buy_date, buy_price, wealth))

    def total_wealth(self):
        for share in self.shares:
            print(share.wealth)
