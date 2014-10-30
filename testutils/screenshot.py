#!/usr/bin/python
"""
@author: Kyle Barry
@copyright: Copyright(c) 2014 VMware, Inc. All rights reserved.
"""

import os
import datetime
from framework.testutils.wait import wait


class screenshot():

    """
    To take a screenshot of the current UI
    """

    def __init__(self, fileName, driver):

        date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        screenshotDir = os.path.abspath("logs")
        fileName = fileName + '-' + date + '.png'

        wait(1)  # wait for animations to complete before taking screenshot
        driver.save_screenshot(screenshotDir + "/" + fileName)
