from basetest import BaseTest

from katello.client.server import ServerRequestError

from mangonel.environment import Environment
from mangonel.organization import Organization
from mangonel.system import System
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
        self.org_api = Organization()
        self.env_api = Environment()
        self.sys_api = System()

        self.start_time = time.time()


    def tearDown(self):
        self.server = None

        self.ellapsed_time = time.time() - self.start_time
        self.logger.info("Test ellapsed time: %s" % self.ellapsed_time)


    def test_create_system_1(self):
        "Creates a new organization with environment and register a system."

        org = self.org_api.create_org()
        self.logger.debug("Created organization %s" % org['name'])
        self.assertEqual(org, self.org_api.organization(org['name']), 'Failed to create and retrieve org.')

        env = self.env_api.create_environment(org, 'Dev', 'Library')
        self.logger.debug("Created environemt %s" % env['name'])
        self.assertEqual(env, self.env_api.environment_by_name(org, 'Dev'))

        env = self.env_api.create_environment(org, 'Testing', 'Dev')
        self.logger.debug("Created environemt %s" % env['name'])
        self.assertEqual(env, self.env_api.environment_by_name(org, 'Testing'))

        env = self.env_api.create_environment(org, 'Release', 'Testing')
        self.logger.debug("Created environemt %s" % env['name'])
        self.assertEqual(env, self.env_api.environment_by_name(org, 'Release'))

        sys1 = self.sys_api.create_system(org, env)
        self.logger.debug("Created system %s" % sys1['uuid'])
        self.assertEqual(sys1['uuid'], self.sys_api.system(sys1['uuid'])['uuid'])
