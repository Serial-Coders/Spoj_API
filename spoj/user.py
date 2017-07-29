import requests
import logging
import bs4

class User(object):
    def __init__(self, uname):
        '''
            Constructor for the User class taking the username
        '''
        self.userName = uname

    def login(self, passW):
        '''
            Used to login to the Spoj,
            its necessary for submitting the problem
        '''
        pass

    #TODO function provided by visi
    def solveCount(self):
        pass

    #TODO function provided by visi
    def attemptCount(self):
        pass

