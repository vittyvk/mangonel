from basetest import BaseTest

from mangonel.environment import Environment
from mangonel.organization import Organization
from mangonel.server import Server

import time
import unittest

class TestOrganizations(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)

        self.server = Server(host=self.host,
                       project=self.project,
                       username=self.user,
                       password=self.password)
        self.org = Organization()
        self.env = Environment()
        
        self.start_time = time.time()


    def tearDown(self):
        self.server = None
        self.ellapsed_time = time.time() - self.start_time
        

    def test_create_org1(self):
        "Creates a new organization."
        
        org = self.org.create_org()
        self.assertEqual(org, self.org.organization(org['name']), 'Failed to create and retrieve org.')


    def test_create_org2(self):
        "Creates a new organization with an initial environment."

        org = self.org.create_org()
        self.assertEqual(org, self.org.organization(org['name']), 'Failed to create and retrieve org.')

        env = self.env.create_environment(org, 'Dev', 'Library')
        self.assertEqual(env, self.env.environment_by_name(org, 'Dev'))


    def test_create_org3(self):
        "Creates a new organization with several environments."

        org = self.org.create_org()
        self.assertEqual(org, self.org.organization(org['name']), 'Failed to create and retrieve org.')

        env = self.env.create_environment(org, 'Dev', 'Library')
        self.assertEqual(env, self.env.environment_by_name(org, 'Dev'))

        env = self.env.create_environment(org, 'Testing', 'Dev')
        self.assertEqual(env, self.env.environment_by_name(org, 'Testing'))

        env = self.env.create_environment(org, 'Release', 'Testing')
        self.assertEqual(env, self.env.environment_by_name(org, 'Release'))
