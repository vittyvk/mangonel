from basetest import BaseTest

from katello.client.server import ServerRequestError

from mangonel.activationkey import ActivationKey
from mangonel.environment import Environment
from mangonel.organization import Organization
from mangonel.product import Product
from mangonel.provider import Provider
from mangonel.repository import Repository
from mangonel.system import System
from mangonel.server import Server

import time
import unittest

class TestActivationKeys(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)

        self.server = Server(host=self.host,
                       project=self.project,
                       username=self.user,
                       password=self.password)
        self.org_api = Organization()
        self.ak_api = ActivationKey()
        self.env_api = Environment()
        self.prd_api = Product()
        self.prv_api = Provider()
        self.repo_api = Repository()
        self.sys_api = System()

        self.start_time = time.time()


    def tearDown(self):
        self.server = None

        self.ellapsed_time = time.time() - self.start_time
        self.logger.info("Test ellapsed time: %s" % self.ellapsed_time)


    def test_get_ak_1(self):
        "Tries to fetch an invalid activationkey."

        org = self.org_api.create()
        self.logger.debug("Created organization %s" % org['name'])
        self.assertEqual(org, self.org_api.organization(org['name']), 'Failed to create and retrieve org.')

        env1 = self.env_api.create_environment(org, 'Dev', 'Library')
        self.logger.debug("Created environemt %s" % env1['name'])
        self.assertEqual(env1, self.env_api.environment_by_name(org, 'Dev'))

        ak1 = self.ak_api.create(env1)
        self.logger.debug("Created activationkey %s" % ak1['name'])
        self.assertEqual(ak1, self.ak_api.activation_key(org, ak1['id']))

        self.assertRaises(ServerRequestError, lambda: self.ak_api.activation_key(org, 10000))


    def test_create_ak_1(self):
        "Creates a new activationkey with no content."

        org = self.org_api.create()
        self.logger.debug("Created organization %s" % org['name'])
        self.assertEqual(org, self.org_api.organization(org['name']), 'Failed to create and retrieve org.')

        env1 = self.env_api.create_environment(org, 'Dev', 'Library')
        self.logger.debug("Created environemt %s" % env1['name'])
        self.assertEqual(env1, self.env_api.environment_by_name(org, 'Dev'))

        ak1 = self.ak_api.create(env1)
        self.logger.debug("Created activationkey %s" % ak1['name'])
        self.assertEqual(ak1, self.ak_api.activation_key(org, ak1['id']))



    def test_create_ak_2(self):
        "Creates a new activationkey and adds a pool."

        org = self.org_api.create()
        self.logger.debug("Created organization %s" % org['name'])
        self.assertEqual(org, self.org_api.organization(org['name']), 'Failed to create and retrieve org.')

        env1 = self.env_api.create_environment(org, 'Dev', 'Library')
        self.logger.debug("Created environemt %s" % env1['name'])
        self.assertEqual(env1, self.env_api.environment_by_name(org, 'Dev'))

        ak1 = self.ak_api.create(env1)
        self.logger.debug("Created activationkey %s" % ak1['name'])
        self.assertEqual(ak1, self.ak_api.activation_key(org, ak1['id']))

        prv = self.prv_api.create_provider(org, 'Provider1')
        self.logger.debug("Created custom provider Provider1")
        self.assertEqual(prv, self.prv_api.provider(prv['id']))

        prd = self.prd_api.create_product(prv, 'Product1')
        self.logger.debug("Created product Product1")
        self.assertEqual(prd['id'], self.prd_api.product(org, prd['id'])['id'])

        repo = self.repo_api.create_repository(org, prd, 'http://hhovsepy.fedorapeople.org/fakerepos/zoo4/', 'Repo1')
        self.logger.debug("Created repositiry Repo1")
        self.assertEqual(repo, self.repo_api.repository(repo['id']))

        # Sync
        self.prv_api.sync(prv['id'])
        self.assertEqual(self.prv_api.provider(prv['id'])['sync_state'], 'finished')
        self.logger.debug("Finished synchronizing Provider1")

        #TODO: There seems to be a delay between sync and pools being available
        pools = self.org_api.pools(org['label'])

        for pool in pools:
            self.ak_api.add_pool(org, ak1['id'], pool['id'])
            self.assertTrue(self.ak_api.has_pool(org, ak1['id'], pool['id']))
            self.logger.debug("Added pool id '%s'' to activationkey '%s'" % (pool['id'], ak1['name']))
