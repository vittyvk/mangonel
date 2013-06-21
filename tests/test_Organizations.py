from basetest import BaseTest

from katello.client.server import ServerRequestError

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
                       password=self.password,
                       port=self.port)
        self.org_api = Organization()
        self.env_api = Environment()

        self.start_time = time.time()


    def tearDown(self):
        self.server = None

        self.ellapsed_time = time.time() - self.start_time
        self.logger.info("Test ellapsed time: %s" % self.ellapsed_time)

    def test_create_org1(self):
        "Creates a new organization."

        org = self.org_api.create()
        self.logger.debug("Created organization %s" % org['name'])
        self.assertEqual(org, self.org_api.organization(org['name']), 'Failed to create and retrieve org.')


    def test_create_org2(self):
        "Creates a new organization and then deletes it."

        org = self.org_api.create()
        self.logger.debug("Created organization %s" % org['name'])
        self.assertEqual(org, self.org_api.organization(org['name']), 'Failed to create and retrieve org.')

        self.logger.info("Deleting organization %s" % org['name'])
        self.org_api.delete(org['name'])
        self.assertRaises(ServerRequestError, lambda: self.org_api.organization(org['name']))


    def test_create_org3(self):
        "Creates a new organization with an initial environment."

        org = self.org_api.create()
        self.logger.debug("Created organization %s" % org['name'])
        self.assertEqual(org, self.org_api.organization(org['name']), 'Failed to create and retrieve org.')

        env = self.env_api.create_environment(org, 'Dev', 'Library')
        self.logger.debug("Created environemt %s" % env['name'])
        self.assertEqual(env, self.env_api.environment_by_name(org, 'Dev'))


    def test_create_org4(self):
        "Creates a new organization with several environments."

        org = self.org_api.create()
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
