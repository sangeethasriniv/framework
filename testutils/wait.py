#!/usr/bin/python
"""
@author: Sangeetha Srinivasan 
@copyright: Copyright(c) 2014 VMware, Inc. All rights reserved.
"""
from time import sleep


class wait():
    """
    To pause test execution
    """
    def __init__(self, seconds=2):

        #self.driver.implicitly_wait(10) // connection issues when using implicit wait, so sticking to the sweet old sleep
        #self.driver.set_page_load_timeout(2) //not yet implemented in appium
        sleep(seconds)
