#!/usr/bin/python
"""
@author: Sangeetha Srinivasan
@copyright: Copyright(c) 2014 VMware, Inc. All rights reserved.
"""
from framework.testexceptions.ElementNotFound import ElementNotFound
from framework.testexceptions.InvalidTestException import InvalidMethodException
from framework.testutils.TestConfig import TestConfig
from appium.webdriver.common.touch_action import TouchAction


class Page():
    """
    Base Page class - All page classes inherit this class to inherit common attributes and methods of the drivers
    """
    def __init__(self):
        """
        Get driver, logger from testConfig
        @param testConfig: object having information about the test, and driver used for test
        This is called by testPage's init method
        """

        self.tConfig = TestConfig()
        self.logger = self.tConfig.logger

        self.iosTest=self.tConfig.iosTest
        self.androidTest=self.tConfig.androidTest
        self.driver = self.tConfig.driver

    def switchToWebView(self):

        """
        Switch to webview when a web page is displayed in the app
        """
        handle = self.driver.window_handles[0]
        self.driver.switch_to_window(handle)

    def deviceBack(self):
        '''
        Method to click device back
        '''
        if(self.androidTest):
            self.driver.back()

    """
    Getters
    """

    """ Elements """
    def getElementByNameContainingText(self, elementHierarchy, text, continue_on_error=False):
        try:
            if(self.iosTest):
                return self.driver.find_element_by_ios_uiautomation(elementHierarchy+".withPredicate(\"name CONTAINS '"+ text +"'\")")
            else:
                raise InvalidMethodException()
        except:
            if (continue_on_error):
                return False
            else:
                raise ElementNotFound(text,self.driver)
         
    def getElementByValueContainingText(self, elementHierarchy, text, continue_on_error=False):
        try:
            if(self.iosTest):
                return self.driver.find_element_by_ios_uiautomation(elementHierarchy+".firstWithPredicate(\"value like '"+ text +"'\")")
            else:
                raise InvalidMethodException()
        except:
            if (continue_on_error):
                return False
            else:
                raise ElementNotFound(text,self.driver)
                          
    def getElementById(self, element_id):
        try:
            return self.driver.find_element_by_id(element_id)
        except:
            raise ElementNotFound(element_id,self.driver)

    def getElementByName(self, element_name, continue_on_error=False):
        try:
            return self.driver.find_element_by_name(element_name)
        except:

            if (continue_on_error):
                return False
            else:
                raise ElementNotFound(element_name,self.driver)

    def getElementByLinkText(self, linkText):
        try:
            return self.driver.find_element_by_link_text(linkText)
        except:
            raise ElementNotFound(linkText,self.driver)

    def getElementByXpath(self, element_path, continue_on_error=False):
        try:
            if (self.iosTest):
                return self.driver.find_element_by_xpath(element_path)
            else:
                raise InvalidMethodException()
        except:
            if (continue_on_error):
                return False
            else:
                raise ElementNotFound(element_path,self.driver)

    def getTextField(self, index):
        try:
            if(self.iosTest):
                textFields = self.driver.find_elements_by_class_name('UIATextField')
                return textFields[index]
            else:
                raise InvalidMethodException()
        except:
                raise ElementNotFound("TextField",self.driver)

    def getTableCell(self, index):
        try:
            if(self.iosTest):
                tableCell = self.driver.find_elements_by_class_name('UIATableCell')
                return tableCell[index]
            else:
                raise InvalidMethodException()
        except:
                raise ElementNotFound("TableCell")

    def getSecureTextField(self, index, continue_on_error=False):
        try:
            if(self.iosTest):
                secureTextFields = self.driver.find_elements_by_class_name('UIASecureTextField')
                return secureTextFields[index]
            else:
                raise InvalidMethodException()
        except:

                if (continue_on_error):
                    return False
                else:
                    raise ElementNotFound("SecureTextField",self.driver)

    def getButton(self, index):
        try:
            if(self.iosTest):
                buttons = self.driver.find_elements_by_class_name('UIAButton')
                return buttons[index]
            else:
                raise InvalidMethodException()
        except:
                raise ElementNotFound("Button",self.driver)

    def getElementByClassName(self, class_name, instance, continue_on_error=False):
        try:
            if(self.androidTest):
                className = self.driver.find_elements_by_class_name(class_name)[instance]
            return className
        except:
            if (continue_on_error):
                return False
            else:
                raise ElementNotFound(class_name,self.driver)

    def tapElementByLocation(self,x,y):
        self.driver.execute_script("mobile: tap", {"x":x, "y":y})

    def getElementsByAndroidUiAutomator(self, element_name,instance):
        try:
            return self.driver.find_elements_by_android_uiautomator('new UiSelector().text("' + element_name + '")')[instance]
        except:
            raise ElementNotFound(element_name,self.driver)

    def getElementByIosUiAutomation(self, element_hierarchy, continue_on_error=False):
        try:
            return self.driver.find_element_by_ios_uiautomation(element_hierarchy)
        except:
            if (continue_on_error):
                return False
            else:
                raise ElementNotFound(element_hierarchy,self.driver)

    """Swipe Functionality"""

    def getElementCenter(self, element):
        '''Usage: center = self.getElementCenter(my_element)
                  x = center['x']
                  y = center['y']                '''

        loc = element.location
        size = element.size

        x = loc['x'] + size['width'] / 2
        y = loc['y'] + size['height'] / 2

        center = {"x": x,
                  "y": y}

        return center

    def swipeElementLeft(self, element):
        # pull element center to get the starting points
        center = self.getElementCenter(element)
        # Calculate ends based on swipe direction
        endx = center['x'] - 100
        endy = center['y']  # no change

        self.swipeElement(center['x'],center['y'],endx,endy)

    def swipeElementRight(self, element):
        # pull element center to get the starting points
        center = self.getElementCenter(element)
        # Calculate ends based on swipe direction
        endx = center['x'] + 100
        endy = center['y']  # no change

        self.swipeElement(center['x'],center['y'],endx,endy)

    def swipeElementUp(self,element):
        # pull element center to get the starting points
        center = self.getElementCenter(element)
        # Calculate ends based on swipe direction
        endx = center['x']
        endy = center['y'] - 200

        self.swipeElement(center['x'],center['y'],endx,endy)

    def swipeElementDown(self,element):
        # pull element center to get the starting points
        center = self.getElementCenter(element)
        # Calculate ends based on swipe direction
        endx = center['x']
        endy = center['y']  + 200

        self.swipeElement(center['x'],center['y'],endx,endy)

    def swipeElement(self,startx,starty,endx,endy):
        duration = 1  # duration of the swipe
        try:
            self.driver.execute_script('mobile: swipe',{'duration': duration, 'startX': startx, 'startY': starty, 'endX': endx, 'endY': endy})
        except:
            print 'SwipeElement Failed!'

    def scrollToElement(self,element,direction):
        try:
            '''Accepted parameters for direction: up and down'''
            params = {"element" : element.id, "direction": direction}
            self.driver.execute_script("mobile: scroll", params)
        except:
            print 'Scroll Failed!'
            
    def longClickElement(self,element):
        try:
            params = {"element" : element.id}
            self.driver.execute_script("mobile: longClick", params)
        except:
            print 'Long Click Failed!'

    def ClickElementCenter(self):
        try:
            startX = self.getElementCenterX()
            startY = self.getElementCenterY()
            self.driver.execute_script("mobile: longClick",{"touchCount": 1, "x": startX, "y": startY})
        except:
            print 'ClickElementCenter Failed'

    """ Attributes """

    def getValue(self, element):
        """ Example return from get_attribute("label") =
            {"status":0,"value":"Subject:, RE: test notification"}
        """

        labelValue = element.get_attribute("label")
        return labelValue[2]

    def longTap(self, element):
        action = TouchAction(self.driver)
        action.long_press(element, 1000).perform()
