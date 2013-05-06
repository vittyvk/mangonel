import os
import unittest

class BaseTest(unittest.TestCase):

    def setUp(self):
        self.host = os.getenv('HOST')
        self.project = os.getenv('PROJECT', None)
        self.user = os.getenv('USER', None)
        self.password = os.getenv('PASSWORD', None)

