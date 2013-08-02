from basetest import BaseTest

from katello.client.server import ServerRequestError

from mangonel.environment import Environment
from mangonel.organization import Organization
from mangonel.system import System
from mangonel.server import Server
from mangonel.csvload import CSVLoad

import time
import unittest
import argparse
import csv


class TestCSVPopulate(BaseTest):

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
        self.csvload = CSVLoad(self.sys_api, self.org_api, self.env_api)

        # Include the main options here so test suites may add their own
        parser = argparse.ArgumentParser()
        parser.add_argument('-dorg', '--org-csv', type=str, dest='org_csv')
        parser.add_argument('-dsys', '--sys-csv', type=str, dest='sys_csv')
        parser.add_argument('--no-cleanup', dest='nocleanup' ,action='store_true', help="Do not remove testing org")
        parser.set_defaults(nocleanup=False)
        [self.args, ignored_args] = parser.parse_known_args()

        self.start_time = time.time()

    def tearDown(self):
        if not self.args.nocleanup:
            self.csvload.delete_organizations(self.args.org_csv)
        self.server = None
        self.ellapsed_time = time.time() - self.start_time
        self.logger.info("Test ellapsed time: %s" % self.ellapsed_time)

    def test_create(self):
        """ Create Orgs and Systems based upon csv files """
        self.csvload.setup_organizations(self.args.org_csv)
        self.csvload.setup_systems(self.args.sys_csv)
