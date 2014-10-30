#!/usr/bin/python
"""
@author: Sangeetha Srinivasan 
@copyright: Copyright(c) 2014 VMware, Inc. All rights reserved.
"""
import imaplib
import email
from framework.testutils.TestLog import TestLog
import sys
import getpass, poplib
from framework.testexceptions.ConnectionFailureException import ConnectionFailureException

class IMAPServer():
    """
    Class to connect to and access IMAP email server
    """
    def __init__(self, emailserver, user, password):
        
        self.emailserver = emailserver
        self.user = user
        self.password= password
        self.logger = TestLog().logger
        self.connectToIMAPServer()
        
    """
    Connect to imap server with imap server address, emailid and password
    """    
    def connectToIMAPServer(self):
        try:
            self.conn = imaplib.IMAP4_SSL(self.emailserver)
            self.conn.login(self.user,self.password)
            self.logger.info("Connected to IMAP EMail server : %s", self.emailserver)
            self.folders = self.getEMailFolders()
            self.connectToInboxFolder()
        except imaplib.IMAP4.error as e:
            raise ConnectionFailureException(self.emailserver, e)
        except:
            self.logger.info("Unable to connect to server : error :  %s", sys.exc_info()[0])
    """
    Close connection with mailbox
    """
    def closeConnection(self):
        self.conn.close()
        
    """
    Get List of folders of the email user
    """
    def getEMailFolders(self):
        return self.conn.list()
    
    """
    Connect to Inbox folder
    """
    def connectToInboxFolder(self):
        self.conn.select("Inbox")
        self.logger.info("Connected to Inbox folder")

    """
    Connect to given folder
    """
    def connectToFolder(self,foldername):
        self.conn.select(foldername)
        self.logger.info("Connected to",foldername)
        
    """
    Get the latest email received in the connected folder
    """
    def getLatestEmail(self):
        
         # return all the uids of emails in the connected folder
        res,uidlist = self.conn.uid('search', None, "ALL")
        
        #Get the first uid in the list
        self.latestEmailUid = uidlist[0].split()[-1]
        
        #Get latest email using the uid
        res, latestEmail = self.conn.uid('fetch', self.latestEmailUid, '(RFC822)')
        rawEmail = latestEmail[0][1]

        #Parse email message to readable format
        self.emailMessage = email.message_from_string(rawEmail)
        self.logger.info("#### Printing the first email in inbox folder")
        self.logger.info("To: %s",self.emailMessage['To'])
        self.logger.info("From: %s", email.Utils.parseaddr(self.emailMessage['From']))
        self.logger.info("Subject: %s",self.emailMessage['Subject'])
        self.logger.info("Message: %s",  self.getFirstTextBlockOfEmail(self.emailMessage))

    """
    Getters for latest email
    """
    def getToFieldOfLatestEmail(self):
        self.getLatestEmail()
        return self.emailMessage['To']

    def getFromFieldOfLatestEmail(self):
        self.getLatestEmail()
        return self.emailMessage['From']

    def getSubjectOfLatestEmail(self):
        self.logger.info("Print subject")
        self.getLatestEmail()
        return self.emailMessage['Subject']

    def getMessageBodyOfLatestEmail(self):
        self.getLatestEmail()
        return self.getFirstTextBlockOfEmail(self.emailMessage)
    
    def getFirstTextBlockOfEmail(self, emailMessage):
        maintype = emailMessage.get_content_maintype()
        if maintype == 'multipart':
            for part in emailMessage.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload(decode=True)
        elif maintype == 'text':
            return emailMessage.get_payload(decode=True)