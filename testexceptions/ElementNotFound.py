#!/usr/bin/python
"""
@author: Sangeetha Srinivasan
@copyright: Copyright(c) 2014 VMware, Inc. All rights reserved.
"""

from framework.testutils.screenshot import screenshot


class ElementNotFound(Exception):
    """
    Element Not found is thrown when the driver is unable to find required element
    """
    def __init__(self, elementName, driver):
        print '\nElement Not Found:', elementName
        screenshot("ElementNotFound",driver)
