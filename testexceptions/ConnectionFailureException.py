#!/usr/bin/python
"""
@author: Sangeetha Srinivasan 
@copyright: Copyright(c) 2014 VMware, Inc. All rights reserved.
"""
class ConnectionFailureException(Exception):
    """
    Adb path is not set in test environment
    """
    def __init__(self, server, e):
        print 'Unable to Connect to Server:',server," : " ,e