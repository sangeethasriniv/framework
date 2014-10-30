#!/usr/bin/python
"""
@author: Sangeetha Srinivasan
@copyright: Copyright(c) 2014 VMware, Inc. All rights reserved.
"""

import logging
import os
from appium import webdriver
from framework.testexceptions.InvalidTestException import InvalidTestException


class Device:
    """
    To get driver capabilities from json and set other environment values needed for test
    """
    def __init__(self):
        self.logger = logging.getLogger('uitest')
        self.dcapability = {}

    def getLogger(self):
        return self.logger

    def getDCapability(self):
        return self.dcapability

    def getApp(self):
        ''' Return app from input'''
        return os.path.abspath(os.getenv("EMAILAPP"))

    def getDriver(self, appiumUrl):
        self.logger.info("Dcapabilities: %s", self.dcapability)
        self.driver = webdriver.Remote(appiumUrl,self.dcapability)
        return self.driver

    # TODO: Add to general library
    def lookupAttr(self, dictionary, attr, customMsg=False, continue_on_error=False):
        try:
            return dictionary[attr]
        except:

            if (customMsg):
                errorMsg = customMsg + ": " + attr
            else:
                errorMsg = "Missing dictionary value: " + attr

            if (continue_on_error):
                print errorMsg
                return False
            else:
                raise InvalidTestException(errorMsg)

    def loadApp(self):
        pass
