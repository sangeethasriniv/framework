#!/usr/bin/python
"""
@author: Sangeetha Srinivasan 
@copyright: Copyright(c) 2014 VMware, Inc. All rights reserved.
"""
import logging
from framework.testutils.CustomDecorators import singleton

@singleton
class TestLog:
    """
    Class to get the logger for uitest
    """
    def __init__(self):          
        self.logger = logging.getLogger('uitest')
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)