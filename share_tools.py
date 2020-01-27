#!/usr/bin/env python
  
__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "January 2020"

class ShareTools:
    def __init__(self, array, reference):
        self.array = array
        self.ref = reference

    def get_maximum(self):
        indmx = self.array.index(max(self.array))
        inlst = self.array.index(self.array[-1])
        if inlst == indmx:
            return True
        else:
            return False

    def get_minimum(self):
        indmn = self.array.index(min(self.array))
        inlst = self.array.index(self.array[-1])
        if inlst == indmn:
            return True
        else:
            return False

    def get_percent(self):
        """ Calculates how far the values of an array are placed
            in percentage with respect to a reference value """
        rng = len(self.array)
        percent = [float(100*(self.array[i]-self.ref)/self.ref) for i in range(rng)]
        return percent

a = [1, 6, 3, 4, 5, 0]
ref = 4
x = ShareTools(a,ref)
print(x.get_percent())
