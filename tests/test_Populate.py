from basetest import BaseTest

from katello.client.server import ServerRequestError
from optparse import OptionParser
from mangonel.csvload import CSVLoad

from mangonel.mangoneloptparse import MangonelOptionParser


class TestCSVPopulate(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)

        # Include the main options here so test suites may add their own
        parser = MangonelOptionParser()
        parser.add_option('--org-csv', type=str, dest='org_csv')
        parser.add_option('--sys-csv', type=str, dest='sys_csv')
        parser.add_option('--no-cleanup', dest='nocleanup', action='store_true', help="Do not remove testing org")
        parser.set_defaults(nocleanup=False)

        self.csvload = CSVLoad(self.sys_api, self.org_api, self.env_api)

        (self.args, ignored_args) = parser.parse_args()

    def tearDown(self):
        if not self.args.nocleanup:
            self.csvload.delete_organizations(self.args.org_csv)
        BaseTest.tearDown(self)

    def test_create(self):
        """ Create Orgs and Systems based upon csv files """
        self.csvload.setup_organizations(self.args.org_csv)
        self.csvload.setup_systems(self.args.sys_csv)

