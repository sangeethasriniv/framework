#!/usr/bin/python
"""
@author: Kyle Barry
@copyright: Copyright(c) 2014 AirWatch, Inc. All rights reserved.
"""
import os
from framework.testutils.Device import Device
from framework.testutils.JsonUtil import JsonUtil
from framework.testutils.CustomDecorators import singleton
from framework.testexceptions.InvalidTestException import InvalidApplicationException


@singleton
class iOS(Device):

    def __init__(self):
        Device.__init__(self)
        self.logger = self.getLogger()

        self.appConfig_json = os.path.abspath("testdata/AppConfigiOS.json")
        self.appConfig_data = JsonUtil(self.appConfig_json).getJsonData()
        
        self.iosConfig_json = os.path.abspath("framework/env/iosConfig.json")
        self.iosConfig_data = JsonUtil(self.iosConfig_json).getJsonData()

        self.DEFAULT_IOS_CONFIG_NAME="ios7.1-xcode5-iphoneSimulator"
        self.iosConfig_name = (os.getenv('IOS_CONFIG')) if (os.getenv('IOS_CONFIG') is not None) else self.DEFAULT_IOS_CONFIG_NAME
        
        self.dcapability = {}
        self.logger.info("Init iOS platform starting...")
        self.iosConfig=self.lookupAttr(self.iosConfig_data,self.iosConfig_name,"ios platform not defined")
        self.dcapability['platformName']    = "iOS"
        self.dcapability['platformVersion'] = self.lookupAttr(self.iosConfig,'platformVersion')
        self.setDevice()

    def setDevice(self):
        if("Simulator" in self.iosConfig_name):
            self.dcapability['deviceName'] = self.lookupAttr(self.iosConfig,'deviceName')
        else:
            self.dcapability['udid'] = self.lookupAttr(self.iosConfig,'udid')

    def loadApp(self, appName):

        ''' Check that app exists in AppConfig '''
        self.appConfig  = self.lookupAttr(self.appConfig_data,appName,"App is not defined")
        self.appPath    = os.path.abspath(self.lookupAttr(self.appConfig,'app'))
        self.appPackage = self.lookupAttr(self.appConfig,'app-package')

        if (os.path.exists(self.appPath)):
            self.dcapability['app']         = self.appPath
            self.dcapability['app-package'] = self.appPackage
        else:
            raise InvalidApplicationException(appName + '. App path is invalid: ' + self.appPath)

        return self.appPackage
