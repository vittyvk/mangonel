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

        # Include the main options here so test suites may add their own
        parser = argparse.ArgumentParser()
        parser.add_argument('-org-csv', '--org-csv', type=str, dest='org_csv')
        parser.add_argument('-sys-csv', '--sys-csv', type=str, dest='sys_csv')
        [self.args, ignored_args] = parser.parse_known_args()

        self.start_time = time.time()


    def tearDown(self):
        self.server = None

        self.ellapsed_time = time.time() - self.start_time
        self.logger.info("Test ellapsed time: %s" % self.ellapsed_time)


    # CSV
    # Name, Label
    #
    def test_setup_organizations(self):
        "Creates organizations based upon CSV"

        if self.args.org_csv is None:
            return

        data = csv.DictReader(open(self.args.org_csv))
        for row in data:
            org = self.org_api.get_or_create_org(row['Name'], row['Label'])
            print org

        return


    # CSV
    # Name
    # Count
    # Org Label
    # Environment Label
    # Groups
    # Virtual
    # Host
    #
    def test_setup_systems(self):
        "Creates systems based upon CSV"

        data = csv.DictReader(open(self.args.sys_csv))
        for row in data:
            org = self.org_api.organization(row['Org Label'])
            env = self.env_api.environment_by_name(org, row['Environment Label'])

            num = 1
            total = int(row['Count'])
            while num < total:
                num += 1
                sys = self.sys_api.get_or_create_system(org, env, row['Name'] % num)

        self.assertEqual(1, 1, 'Failed')
