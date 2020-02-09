#!/usr/bin/env python
  
__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "February 2020"

from share import Share

def main():
    zeiss = Share("AFX.DE","2019-10-23","93.123","5005.8")
    apple = Share("APC.DE","2019-03-01","153.217","5010.7")
    print(zeiss.get_close_price())

if __name__ == "__main__":
    main()
