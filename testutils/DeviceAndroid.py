#!/usr/bin/python
"""
* Author: Kyle Barry
* Copyright (C) 2014 AirWatch, LLC. All rights reserved.
* This product is protected by copyright and intellectual property laws in the United States and other countries as well as by international treaties.
* AirWatch products may be covered by one or more patents listed at http://www.vmware.com/go/patents.
"""

import os
import subprocess
from framework.testutils.Device import Device
from framework.testutils.CustomDecorators import singleton
from framework.testutils.JsonUtil import JsonUtil
from subprocess import Popen, PIPE, STDOUT, CalledProcessError
from framework.testexceptions.AdbPathNotSetException import AdbPathNotSetException
from framework.testexceptions.InvalidTestException import InvalidApplicationException
from framework.testutils.wait import wait


@singleton
class Android(Device):

    def __init__(self):
        Device.__init__(self)
        self.logger = self.getLogger()

        self.appConfig_json = os.path.abspath("testdata/AppConfigAndroid.json")
        self.appConfig_data = JsonUtil(self.appConfig_json).getJsonData()

        self.dcapability = {}
        self.selendroid = os.getenv('SELENDROID')
        self.logger.info("Init Android platform starting...")

        ''' Use Selendroid for API level <= 16 '''
        if (self.selendroid == 1):
            self.logger.info("Activating Selendroid driver.")
            self.dcapability['automationName'] = "Selendroid"
            self.loadKeyStore()

        self.dcapability['platform']        = "Mac"
        self.dcapability['platformName']    = self.getPlatformName().lower()
        self.dcapability['platformVersion'] = self.getPlatformVersion()
        self.dcapability['deviceName']      = self.getAndroidDeviceName()

    ''' Device Methods '''

    def getPlatformName(self):
        return "Android"

    def getPlatformVersion(self):
        ''' Change device OS version to actual version if available '''
        if (os.getenv("ANDROID_OS_VERSION") is not None):
            return os.getenv("ANDROID_OS_VERSION").rstrip()
        else:
            return "4.3"

    def loadKeyStore(self):

        ''' Get keystore information '''
        self.keyStorePath=os.path.abspath(os.getenv('KEYSTOREPATH')) if (os.getenv('KEYSTOREPATH') is not None) else None

        if (self.keyStorePath):
            self.logger.info("Custom keystore: " + self.keyStorePath)
        else:
            self.logger.info("No keystore found; continuing without signing")

        ''' Set server variables '''
        if (self.keyStorePath is not None):
            self.dcapability['useKeystore'] = "true"
            self.dcapability['keystorePath'] = self.keyStorePath
            self.dcapability['keystorePassword'] = "android"

    ''' App Methods '''

    def loadApp(self, appName):

        ''' Check that app exists in AppConfig '''
        self.appConfig = self.lookupAttr(self.appConfig_data,appName,"App is not defined")
        self.androidPackage = self.lookupAttr(self.appConfig,'androidPackage')

        ''' INSTALL App or ADD app to dcaps '''
        if (appName != "Settings"):
            self.appPath = os.path.abspath(self.lookupAttr(self.appConfig,'app'))

            if (os.path.exists(self.appPath)):
                if (self.selendroid == 1):
                    self.dcapability['app'] = self.appPath
                else:
                    #self.uninstallApp(self.androidPackage)
                    #self.installApp(self.appPath)

                    if (self.lookupAttr(self.appConfig, 'wait',continue_on_error=True)):
                        waitTime = self.lookupAttr(self.appConfig, 'wait')
                        wait(int(waitTime))

            else:
                raise InvalidApplicationException(appName + '. App path is invalid: ' + self.appPath)

        self.dcapability['androidPackage'] = self.androidPackage
        self.dcapability['appActivity']    = self.lookupAttr(self.appConfig,'appActivity')

        if (self.lookupAttr(self.appConfig,'appWaitActivity',continue_on_error=True)):
            self.dcapability['appWaitActivity'] = self.lookupAttr(self.appConfig,'appWaitActivity')

        ''' Return packageID so app can be uninstalled if needed '''
        return self.androidPackage

    def installApp(self, appPath):
        cmd = self.getADBPath() + " install " + appPath
        self.logger.info("Installing app: %s", appPath)
        success = self.cmdExec(cmd)
        self.logger.info("Install...%s", success)
        return success

    def uninstallApp(self, packageID):
        cmd = self.getADBPath() + " uninstall " + packageID
        self.logger.info("Uninstalling app: %s", packageID)
        success = self.cmdExec(cmd)
        self.logger.info("Uninstall...%s", success)
        return success

    # TODO: Need to move this method to a different class which holds all the utils
    def exeExists(self,cmd):
        ''' cmd name of the host utility to be checked '''
        p = subprocess.call(["type", cmd],stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0
        return p

    def cmdExec(self, cmd):
        try:
            return Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read()

        except CalledProcessError, e:
            err = e.output
            self.logger.info(err)

    def getADBPath(self):
        ''' If adb exists in path execute adb command as such , else get adb from ADB_PATH environment variable'''

        if (self.exeExists("adb")):
            self.adbPath = "adb "
        elif (os.getenv('ADB_PATH') is not None):
            self.adbPath = os.getenv('ADB_PATH')
        else:
            raise AdbPathNotSetException

        return self.adbPath

    def getAndroidDeviceName(self):
        ADBCOMMAND = self.getADBPath() + " shell getprop ro.product.device"
        deviceName = self.cmdExec(ADBCOMMAND)
        return deviceName
