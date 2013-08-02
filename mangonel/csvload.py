import csv


class CSVLoad():
    """ Load orgs/systems from csv files """
    def __init__(self, sys_api, org_api, env_api):
        self.sys_api = sys_api
        self.org_api = org_api
        self.env_api = env_api

    def setup_organizations(self, csv_file):
        "Creates organizations based upon CSV"
        # CSV:
        # Name, Label
        #

        if csv_file is None:
            return

        data = csv.DictReader(open(csv_file))
        for row in data:
            org = self.org_api.get_or_create_org(row['Name'], row['Label'])

        return

    def delete_organizations(self, csv_file):
        "Removes organizations based upon CSV"
        # CSV:
        # Name, Label
        #
        if csv_file is None:
            return
        data = csv.DictReader(open(csv_file))
        for row in data:
            org = self.org_api.delete(row['Name'])

        return

    def setup_systems(self, csv_file):
        "Creates systems based upon CSV"
        # CSV:
        # Name
        # Count
        # Org Label
        # Environment Label
        # Groups
        # Virtual
        # Host
        #

        if csv_file is None:
            return

        # Accumulate host systems so guests can be stored and associted (mimicing virt-who)
        #
        host_systems = {}

        data = csv.DictReader(open(csv_file))
        for row in data:
            org = self.org_api.organization(row['Org Label'])
            env = self.env_api.environment_by_name(org, row['Environment Label'])

            num = 0
            total = int(row['Count'])
            while num < total:
                num += 1

                sys = self.sys_api.get_or_create_system(org, env, self._namify(row['Name'], num))

                self._system_update(sys, num, row)

                if row['Host']:
                    host_systems = self._set_host_guest(host_systems, org, env, sys, num, row)

                self.sys_api.checkin(sys)
                self.sys_api.api.refresh_subscriptions(sys['uuid'])

    @staticmethod
    def _namify(name, row):
        try:
            return name % row
        except TypeError:
            return name

    def _system_update(self, sys, num, row):
        facts = {}
        if row['Virtual'] == 'Yes':
            facts['virt.is_guest'] = True
            facts['virt.uuid'] = self._namify(row['Name'], num)
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
        self.sys_api.api.update(sys['uuid'], params)

    def _set_host_guest(self, host_systems, org, env, sys, num, row):
        host_name = self._namify(row['Host'], num)
        if not host_name in host_systems:
            host = self.sys_api.get_or_create_system(org, env, host_name)
            host_systems[host_name] = [host['uuid']]

        #host_systems[host_name].append(sys['uuid'])
        host_systems[host_name].append(self._namify(row['Name'], num))

        params = {}
        params['guestIds'] = host_systems[host_name][1::]
        self.sys_api.api.update(host_systems[host_name][0], params)
        return host_systems
