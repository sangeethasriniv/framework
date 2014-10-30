#!/usr/bin/python
"""
@author: Sangeetha Srinivasan
@copyright: Copyright(c) 2014 VMware, Inc. All rights reserved.
"""

import logging
import os
from framework.testexceptions.InvalidTestException import InvalidTestEnvException
from framework.testutils.DeviceAndroid import Android
from framework.testutils.DeviceiOS import iOS
from framework.testutils.CustomDecorators import singleton


@singleton
class LoadTestEnv:
    """
    To get driver capabilities from json and set other environment values needed for test
    """
    def __init__(self):
        self.logger = logging.getLogger('uitest')
        self.logger.info("Init Load Test Env ****")
        self.initTestEnv()
        self.loadPath()
        self.loadAppiumServer()
        self.loadDevice()
        self.logger.info("End Load Test Env ****")

    def initTestEnv(self):
        '''Set Test Environment '''
        self.IOS_ENV = 'ios'
        self.ANDROID_ENV = 'android'
        self.iosTest = False
        self.androidTest = False

        ''' By default the test is set for ios simulator, self.DEFAULT_ENV to self.ANDROID_ENV, to run default android tests'''
        self.DEFAULT_ENV = self.ANDROID_ENV

        ''' Check if there is any preferred test is set in the environment variable ENV and set the test environment '''
        '''     if nothing available set to default '''
        self.env = os.getenv('ENV').lower() if (os.getenv('ENV') is not None) else self.DEFAULT_ENV
        self.logger.info("Test Env: %s", self.env)

    def loadPath(self):
        ''' Set default Automation Path '''
        self.DEFAULT_AUTOROOT = os.path.abspath(os.path.join(os.getcwd()))
        self.autoRoot = os.path.abspath(os.getenv('AUTOMATIONROOT')) if (os.getenv('AUTOMATIONROOT') is not None) else self.DEFAULT_AUTOROOT
        os.environ['AUTOMATIONROOT'] = self.autoRoot
        self.logger.info("Automation Root: %s", self.autoRoot)

    def loadAppiumServer(self):
        ''' Set server name to variable in case we want to replace later '''
        serverName=os.getenv("APPIUMSERVER")

        ''' Set the appium server address'''
        self.appiumServer='localhost'
        self.appiumServer=serverName if (serverName is not None) else self.appiumServer

        self.appiumUrl='http://' + self.appiumServer + ':4723/wd/hub'
        self.logger.info("Appium Server: %s", self.appiumServer)
        self.logger.info("Appium URL: %s",self.appiumUrl)

    def loadDevice(self):
        ''' Get device settings and load driver '''
        if (self.env == self.IOS_ENV):
            self.iosTest = True
            self.device  = iOS()
        elif (self.env == self.ANDROID_ENV):
            self.androidTest = True
            self.device = Android()
        else:
            ''' Throw error because the calculated environment is not valid '''
            raise InvalidTestEnvException
