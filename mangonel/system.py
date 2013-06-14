from common import *

import datetime
import json
import requests
import sys
import time

try:
    from katello.client.api.system import SystemAPI
except ImportError, e:
    print "Please install Katello CLI package."
    sys.exit(-1)


class System():
    api = SystemAPI()
    
    def create_system(self, org, env, name=None, ak=None, type='system',
                      release=None, sla=None, facts=None, view_id=None, installed_products=None):

        if name is None:
            name = "%s.example.com" % generate_name(8)

        if facts is None:
            facts = generate_facts(name)

        return self.api.register(name, org['label'], env['id'], ak, type, release, sla, facts, view_id, installed_products)


    def delete_system(self, system):
        return self.api.unregister(system['uuid'])

    
    def checkin(self, system):
        return self.api.checkin(system['uuid'])


    def system(self, system_uuid):
        return self.api.system(system_uuid)

    
    def update_packages(self, system, packages=None):

        if packages is None:
            packages = packages_list()

        return self.api.update_packages(system['uuid'], packages)


    def available_pools(self, sId, match_system=False, match_installed=False, no_overlap=False):
        return self.api.available_pools(sId, match_system, match_installed, no_overlap)['pools']


    def pool(self, sId, product_name):
        pools = self.available_pools(sId)

        return [p for p in pools if p['productName'] == product_name]

    def subscribe(self, sId, product_name, pool=None, qty=1):

        if pool is None:
            pool = self.pool(sId, product_name)
            pool = pool[0]['id']

        return self.api.subscribe(sId, pool, qty)
