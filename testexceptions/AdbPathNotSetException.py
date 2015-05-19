#!/usr/bin/python
"""
@author: Sangeetha Srinivasan 
@copyright: Copyright(c) 2014 VMware, Inc. All rights reserved.
"""
class AdbPathNotSetException(Exception):
    """
    Adb path is not set in test environment
    """
    def __init__(self):
        print 'ADB_PATH is not set in test environmenti#####'
