#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "December 2019"

import numpy as np

def weighted_mean(proportion,data_set):
    maximum = float(max(proportion))
    wgts = []
    for i in range(len(data_set)):
        coeff = float(proportion[i]) / maximum
        wgts.append(coeff)
    wm = np.average(data_set, weights=wgts)
    return wm
