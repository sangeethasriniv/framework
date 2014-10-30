#!/usr/bin/python
"""
@author: Sangeetha Srinivasan
@copyright: Copyright(c) 2014 VMware, Inc. All rights reserved.
"""


class InvalidTestEnvException(Exception):
    """
    Invalid test exception is thrown when proper test environment is not set
    """
    def __init__(self):
        print "Specify [android, iphone, iphonesimulator] as -e testenv OR supply a JSON with Device name same as testenv"


class InvalidJSONException(Exception):
    """
    Invalid JSON exception is thrown when the values in json is not properly formatted
    """
    def __init__(self):
        print "Incorrect JSON format: Check json values / Use a good JSON Editor"


class InvalidMethodException(Exception):
    """
    Invalid Method Exception is thrown when trying to access a method that is not supported by the test platform
    """
    def __init__(self):
        print "This method is not supported in this test platform"


class InvalidApplicationException(Exception):
    """
    Invalid Application Exception is thrown when initialized values for an app are missing or invalid
    """
    def __init__(self, appName):
        print "Unable to initialize app: ", appName


class InvalidTestException(Exception):
    """
    Generic exception for invalid test scenarios
    """
    def __init(self, msg):
        print msg
