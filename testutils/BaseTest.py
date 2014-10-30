#!/usr/bin/python
"""
@author: Sangeetha Srinivasan
@copyright: Copyright(c) 2014 VMware, Inc. All rights reserved.
"""
import unittest
from framework.testutils.TestConfig import TestConfig


class BaseTest(unittest.TestCase):
    """
    Base Test class - All test classes inherit this class for general test setup
    """
    @classmethod
    def setUpClass(cls):
        cls.tConfig = TestConfig()
        cls.logger = cls.tConfig.logger
        cls.iosTest= cls.tConfig.iosTest
        cls.androidTest= cls.tConfig.androidTest

    def setUp(self):
        self.logger.info("Start: %s",self.id())

    def tearDown(self):
        self.logger.info("End: %s",self.id())

    def failTest(self,e):
        self.fail("failed ::{}::{})".format(type(e), e))

    @classmethod
    def tearDownClass(cls):
        cls.logger.info("End Test")

if __name__ == '__main__':
    unittest.main()
