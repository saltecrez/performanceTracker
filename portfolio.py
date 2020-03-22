#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "February 2020"

import collections
import numpy as np
from share import Share 
from json_parser import SharesJsonParser

rj = SharesJsonParser()

class SortOutShares(object):
    def __init__(self):
        self.shares_list = rj._get_shares()

    def weighted_mean(self,proportion,data_set):
        maximum = float(max(proportion))
        wgts = []
        for i in range(len(data_set)):
            coeff = float(proportion[i]) / maximum
            wgts.append(coeff)
        wm = np.average(data_set, weights=wgts)
        return wm

    def find_all_labels(self):
        labels = [i[0] for i in self.shares_list]
        return labels

    def find_multiple_labels(self):
        labels = [i[0] for i in self.shares_list]
        counter = collections.Counter(labels)
        multiple_labels = []
        for label, count in counter.items():
            if count > 1:
                multiple_labels.append(label)
        return multiple_labels

    def multiple_wealth(self, wlist):
        tw = 0.0
        for i in wlist:
            tw += float(i)
        return tw

    def multiple_buyprice(self, wlist, bplist):
        buy_price = self.weighted_mean(wlist, bplist)
        return buy_price

    def multiple_date(self, dlist):
        d = min(dlist)
        return d

    def join_shares(self, label):
        wl = []; bpl = []; dl = []
        for i in self.shares_list:
            if label  == i[0]:
                wl.append(float(i[3]))
                bpl.append(float(i[2]))
                dl.append(i[1])
        md = self.multiple_date(dl)
        mbp = self.multiple_buyprice(wl,bpl)
        mw = self.multiple_wealth(wl)
        return md, mbp, mw

class Portfolio(object):
    def __init__(self):
        self.shares = []

    def add_share(self, label, buy_date, buy_price, wealth):
        self.shares.append(Share(label, buy_date, buy_price, wealth))

    def total_wealth(self):
        tw = 0.0
        for share in self.shares:
            tw += float(share.wealth)
        return round(tw,2)

    def total_yield_perc(self):
        pass

    def total_yield(self):
        pass

if __name__ == "__main__":
    print(SortOutShares().join_shares('CM9.MI'))
