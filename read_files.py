#!/usr/bin/env python
  
__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "January 2020"

import os
import json

class ReadFiles:
    def __init__(self, filename):
        self.filename = filename

    def read_json(self):
        json_config_file_path = '%s/%s' % (os.getcwd(),self.filename)
        config_properties = {}
        with open(json_config_file_path) as data_file:
            config_properties = json.load(data_file)
        return config_properties
    
    def read_csv(self):
        rowlist = []
        with open(self.filename) as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=',')
            for row in csv_reader:
                rowlist.append(row)
        return rowlist

a = 'conf.json'
x = ReadFiles(a)
print(x.read_json())
