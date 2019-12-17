#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "December 2019"

from datetime import datetime

def get_dates(d):
    dates = []
    date_format = '%Y-%m-%d'
    for i in d.index:
        strip = datetime.strftime(i, date_format)
        restrip = datetime.strptime(strip, date_format)
        dates.append(restrip)
    return dates 
