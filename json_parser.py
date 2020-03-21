#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "January 2020"

import os
import json
import collections
from utilities import LoggingClass
from utilities import MissingConfParameter

log = LoggingClass('',True).get_logger()

class SharesJsonParser(object):
    def _create_dictionary(self):
        try:
            json_config_file_path = '%s/%s' % (os.getcwd(), 'conf.json')
            config_properties = {}
            with open(json_config_file_path) as data_file:
                config_properties = json.load(data_file)
            return config_properties
        except Exception as e:
            log.error("{0}".format(e))
            exit(1)

    def get_recipient(self):
        try:
            recipient = self._create_dictionary().get("email")
            if recipient is None:
                raise MissingConfParameter('email')
            return recipient
        except MissingConfParameter as e:
            log.error("{0}".format(e))
            exit(1)

    def get_sender(self):
        try:
            sender = self._create_dictionary().get("sender")
            if sender is None:
                raise MissingConfParameter('sender')
            return sender
        except MissingConfParameter as e:
            log.error("{0}".format(e))

    def get_smtp_host(self):
        try:
            smtp_host = self._create_dictionary().get("smtp_host")
            if smtp_host is None:
                raise MissingConfParameter('smtp_host')
            return smtp_host
        except MissingConfParameter as e:
            log.error("{0}".format(e))
            exit(1)

    def _get_shares(self):
        try:
            shares_dict = self._create_dictionary().get("shares")
            shares_list = []
            [shares_list.append([i.get("label"),i.get("buydate"),i.get("buyprice"),i.get("wealth")]) for i in shares_dict]
            return shares_list
        except MissingConfParameter as e:
            log.error("{0}".format(e))
            exit(1)

    def _find_multiple_labels(self):
        labels = [i[0] for i in self._get_shares()]
        counter = collections.Counter(labels)
        multiple_labels = []
        multiple_counts = []
        for label, count in counter.items():
            if count > 1:
                multiple_labels.append(label)
                multiple_counts.append(count)
        return multiple_labels, multiple_counts

    def create_multiple_shares(self):
        for i in self._get_shares():
            if i[0] in self._find_multiple_labels():
                print(i)

if __name__ == "__main__":
    #SharesJsonParser(a).create_multiple_shares()
    #print(JsonParser(a).get_tuples_list())
    SharesJsonParser()._get_shares()
