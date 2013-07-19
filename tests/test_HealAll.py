from basetest import BaseTest

from katello.client.server import ServerRequestError

from mangonel.environment import Environment
from mangonel.organization import Organization
from mangonel.system import System
from mangonel.server import Server

import time
import unittest
import argparse
import csv


class TestHealAll(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)

        self.server = Server(host=self.host,
                       project=self.project,
                       username=self.user,
                       password=self.password,
                       port=self.port)
        self.org_api = Organization()
        self.env_api = Environment()
        self.sys_api = System()

        # Include the main options here so test suites may add their own
        parser = argparse.ArgumentParser()
        parser.add_argument('-dorg', '--org-label', type=str, dest='org_label')
        [self.args, ignored_args] = parser.parse_known_args()

        self.start_time = time.time()


    def tearDown(self):
        self.server = None

        self.ellapsed_time = time.time() - self.start_time
        self.logger.info("Test ellapsed time: %s" % self.ellapsed_time)


    def test_heal_org(self):
        "Refresh subscriptions in whole org"

        if self.args.org_label is None:
            return

        systems = self.sys_api.systems_by_org(self.args.org_label)
        for system in systems:
            self.sys_api.refresh_subscriptions(system['uuid'])

