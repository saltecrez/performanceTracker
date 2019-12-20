#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "October 2019"

""" Calculates how far the values of an array are placed in 
    percentage with respect to a reference value """


def percent_calculator(array,reference):
    percent = []
    for i in range(len(array)):
        delta = float(array[i])-float(reference)
        dummy = 100*delta/float(reference)
        percent.append(dummy)
    return percent
