#!/usr/bin/python
"""
@author: Sangeetha Srinivasan
@copyright: Copyright(c) 2014 VMware, Inc. All rights reserved.
"""
import os
from framework.testutils.LoadTestEnv import LoadTestEnv
from framework.testutils.TestLog import TestLog
from framework.testutils.CustomDecorators import singleton


@singleton
class TestConfig:
    '''
    Class to hold driver, driver parameters and general test data
    '''
    def __init__(self):
        self.logger = TestLog().logger
        testEnv = LoadTestEnv()
        self.iosTest = testEnv.iosTest
        self.androidTest = testEnv.androidTest
        self.appiumUrl = testEnv.appiumUrl
        self.device = testEnv.device
        if (self.androidTest):
            self.deviceName = self.device.getAndroidDeviceName()

    def setDriver(self):
        self.driver = self.device.getDriver(self.appiumUrl)

    def setApp(self, appName):
        self.logger.info("Launch app: %s", appName)
        self.appID = self.device.loadApp(appName)
        self.setDriver()

    def cleanApp(self, forceClean=False):
        clean = os.getenv("CLEAN")

        if (self.androidTest):
            if (clean == "yes" or forceClean):
                self.device.uninstallApp(self.appID)

    def quitDriver(self):
        self.driver.quit()
