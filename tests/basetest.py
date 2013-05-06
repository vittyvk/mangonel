import os
import unittest

class BaseTest(unittest.TestCase):

    def setUp(self):
        self.host = os.getenv('HOST')
        self.project = os.getenv('PROJECT')
        self.user = os.getenv('USERNAME')
        self.password = os.getenv('PASSWORD')

