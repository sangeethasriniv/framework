#!/usr/bin/python
"""
@author: Sangeetha Srinivasan 
@copyright: Copyright(c) 2014 VMware, Inc. All rights reserved.
"""
class LoginFailure(Exception):
    """
    Login Failure Raised when login action sequence has errors 
    """
    def __init__(self):
        print "Login Failed"