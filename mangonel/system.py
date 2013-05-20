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
    
    def create_system(self, name, org, env, ak=None, type='system',
                      release=None, sla=None, facts=None, view_id=None, installed_products=None):

        if name is None:
            name = generate_name(8)

        if facts is None:
            facts = generate_facts(name)

        return self.api.register(name, org['label'], env['id'], ak, type, release, sla, facts, view_id, installed_products)


    def delete_system(self, system):
        return self.api.unregister(system['uuid'])

    
    def checkin(self, system):
        return self.api.checkin(system['uuid'])


    def system(self, system_id):
        return self.api.system(system_id)

    
    def update_packages(self, system, packages=None):

        if packages is None:
            continue

        return self.api.update_packages(system['uuid'], packages)
