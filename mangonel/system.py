from common import *

import datetime
import json
import sys
import time

try:
    from katello.client.api.system import SystemAPI
except ImportError, e:
    print "Please install Katello CLI package."
    sys.exit(-1)


class System(SystemAPI):

    def __init__(self):
        super(System, self).__init__()

    def create(self, org, env, name=None, ak=None, type='system',
                      release=None, sla=None, facts=None, view_id=None, installed_products=None):

        if name is None:
            name = "%s.example.com" % generate_name(8)

        if facts is None:
            facts = generate_facts(name)

        sys1 = super(System, self).register(name, org['label'], env['id'], ak, type, release, sla, facts, view_id, installed_products)

        logger.debug("Created system '%s'" % sys1['name'])

        return sys1


    def get_or_create_system(self, org, env, name=None, ak=None, type='system',
                             release=None, sla=None, facts=None, view_id=None, installed_products=None):

        sys = None

        query = {}
        if name is not None:
            query['name'] = name

        if query != {}:
            systems = super(System, self).systems_by_env(env['id'], query)
            if systems != []:
                sys = systems[0]
            else:
                sys = self.create(org, env, name, ak, type,
                                         release, sla, facts, view_id, installed_products)

        return sys

    def delete_system(self, system):
        return super(System, self).unregister(system['uuid'])

    def checkin(self, system):
        return super(System, self).checkin(system['uuid'])

    def update_packages(self, system, packages=None):

        if packages is None:
            packages = packages_list()

        return super(System, self).update_packages(system['uuid'], packages)

    def available_pools(self, sId, match_system=False, match_installed=False, no_overlap=False):
        return super(System, self).available_pools(sId, match_system, match_installed, no_overlap)['pools']

    def subscribe(self, sId, pool=None, qty=1):
        return super(System, self).subscribe(sId, pool, qty)
