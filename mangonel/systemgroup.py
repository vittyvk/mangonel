from katello.client.server import ServerRequestError

from common import *

import datetime
import json
import sys
import time

try:
    from katello.client.api.system_group import SystemGroupAPI
except ImportError, e:
    print "Please install Katello CLI package."
    sys.exit(-1)


class SystemGroup():
    api = SystemGroupAPI()


    def system_groups(self, org):
        return self.api.system_groups(org['label'])


    def system_group(self, org, system_group_id, query=None):
        return self.api.system_group(org['label'], system_group_id, query)


    def system_group_systems(self, org, system_group_id, query=None):
        return self.api.system_group_systems(org['label'], system_group_id, query)


    def create(self, org, name=None, description=None, max_systems=-1):

        if name is None:
            name = "%s-system-group" % generate_name()

        if description is None:
            description = "Generated automatically."

        return self.api.create(org['label'], name, description, max_systems)


    def copy(self, org, system_group_id, new_name=None, description=None, max_systems=-1):

        if new_name is None:
            new_name = "%s-copied-system-group" % generate_name()

        if description is None:
            description = "Copied automatically."

        return self.api.copy(org['label'], system_group_id, new_name, description, max_systems)


    def update(self, org, system_group_id, name=None, description=None, max_systems=-1):
        return self.api.delete(org['label'], )


    def delete(self, org, system_group_id, delete_systems=False):
        return self.api.delete(org['label'], system_group_id, delete_systems)


    def add_systems(self, org, system_group_id, system_ids):
        return self.api.add_systems(org['label'], system_group_id, system_ids)


    def remove_systems(self, org, system_group_id, system_ids):
        return self.api.remove_systems(org['label'], system_group_id, system_ids)


    def install_packages(self, org, system_group_id, packages):
        return self.install_packages(org['label'], system_group_id, packages)


    def update_packages(self, org, system_group_id, packages):
        return self.api.update_packages(org['label'], system_group_id, packages)


    def remove_packages(self, org, system_group_id, packages):
        return self.api.remove_packages(org['label'], system_group_id, packages)


    def install_package_groups(self, org, system_group_id, packages):
        return self.install_package_groups(org['label'], system_group_id, packages)


    def update_package_groups(self, org, system_group_id, packages):
        return self.api.update_package_groups(org['label'], system_group_id, packages)


    def remove_package_groups(self, org, system_group_id, packages):
        return self.api.remove_package_groups(org['label'], system_group_id, packages)


    def errata(self, org, system_group_id, type_in=None):
        return self.api.errata(org['label'], system_group_id, type_in)


    def install_errata(self, org, system_group_id, errata):
        return self.api.install_errata(org['label'], system_group_id, errata)


    def update_systems(self, org, system_group_id, env, view):
        return self.api.update_systems(org['label'], system_group_id, env['id'], view['id'])
