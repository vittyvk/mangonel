from basetest import BaseTest

from katello.client.server import ServerRequestError
from mangonel.mangoneloptparse import MangonelOptionParser
import csv
import time


class TestCSVPopulate(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)

        # Include the main options here so test suites may add their own
        parser = MangonelOptionParser()
        parser.add_option('--org-csv', type=str, dest='org_csv')
        parser.add_option('--sys-csv', type=str, dest='sys_csv')
        (self.args, ignored_args) = parser.parse_args()

        self.start_time = time.time()


    def namify(self, name, row):
        try:
            return name % row
        except TypeError:
            return name


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

        if self.args.sys_csv is None:
            return

        # Accumulate host systems so guests can be stored and associted (mimicing virt-who)
        #
        host_systems = {}

        data = csv.DictReader(open(self.args.sys_csv))
        for row in data:
            org = self.org_api.organization(row['Org Label'])
            env = self.env_api.environment_by_name(org['label'], row['Environment Label'])

            num = 0
            total = int(row['Count'])
            while num < total:
                num += 1

                sys = self.sys_api.get_or_create_system(org, env, self.namify(row['Name'], num))

                self.system_update(sys, num, row)

                if row['Host']:
                    host_systems = self.set_host_guest(host_systems, org, env, sys, num, row)

                self.sys_api.checkin(sys)
                self.sys_api.refresh_subscriptions(sys['uuid'])

        self.assertEqual(1, 1, 'Failed')


    def system_update(self, sys, num, row):
        facts = {}
        if row['Virtual'] == 'Yes':
            facts['virt.is_guest'] = True
            facts['virt.uuid'] = self.namify(row['Name'], num)
        else:
            facts['virt.is_guest'] = False
        facts['cpu.core(s)_per_socket'] = row['Cores']
        facts['cpu.cpu_socket(s)'] = row['Sockets']
        facts['memory.memtotal'] = row['RAM'] + 'GB'
        facts['uname.machine'] = row['Arch']
        facts['system.certificate_version'] = '3.2'
        if row['OS'].find(' ') != -1:
            [facts['distribution.name'], facts['distribution.version']] = row['OS'].split(' ')
        else:
            facts['distribution.name'], facts['distribution.version'] = ('RHEL', row['OS'])

        installed_products = []
        if row['Products']:
            for product in row['Products'].split(','):
                [product_number, product_name] = product.split('|')
                installed_products.append({'productId': int(product_number), 'productName': product_name})

        params = {}
        params['facts'] = facts
        params['installedProducts'] = installed_products
        self.sys_api.update(sys['uuid'], params)


    def set_host_guest(self, host_systems, org, env, sys, num, row):
        host_name = self.namify(row['Host'], num)
        if not host_name in host_systems:
            host = self.sys_api.get_or_create_system(org, env, host_name)
            host_systems[host_name] = [host['uuid']]

        #host_systems[host_name].append(sys['uuid'])
        host_systems[host_name].append(self.namify(row['Name'], num))

        params = {}
        params['guestIds'] = host_systems[host_name][1::]
        self.sys_api.update(host_systems[host_name][0], params)
        return host_systems
