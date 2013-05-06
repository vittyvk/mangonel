from mangonel.api import *

import time
import unittest

class TestOrganizations(unittest.TestCase):

    def setUp(self):
        self.api = api()
        self.start_time = time.time()


    def tearDown(self):
        self.api = None
        self.ellapsed_time = time.time() - self.start_time
        

    def test_create_org1(self):
        "Creates a new organization."
        
        org = create_org()


    def test_create_org2(self):
        "Creates a new organization with an initial environment."

        org = create_org()

        env = create_env(org, 'Dev', 'Library')


