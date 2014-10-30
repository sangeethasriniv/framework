#!/usr/bin/python
"""
@author: Sangeetha Srinivasan 
@copyright: Copyright(c) 2014 VMware, Inc. All rights reserved.
"""
import json
from pprint import pprint
from framework.testexceptions.InvalidTestException import InvalidJSONException


def _decode_dict(data):
    """
    json.loads gets the data from json file in unicode format
    The webdriver accepts data in utf-8 format 
    This method is to convert data from unicode to utf-8
    """
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        rv[key] = value
    return rv

class JsonUtil():
    """
    Json operations
    """
    def __init__(self, jsonPath):
        self.jsonPath=jsonPath

    def getJsonData(self):
        with open(self.jsonPath) as jsonData:
            try:
                return json.load(jsonData, object_hook=_decode_dict)
            except:
                raise InvalidJSONException