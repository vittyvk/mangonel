from katello.client.server import ServerRequestError

from common import *

import datetime
import json
import requests
import sys
import time

try:
    from katello.client.api.activation_key import ActivationKeyAPI
except ImportError, e:
    print "Please install Katello CLI package."
    sys.exit(-1)


class ActivationKey():
    api = ActivationKeyAPI()

    def create(self, env, name=None, description=None, limit=-1, cvId=None):

        if name is None:
            name = "%s-key" % generate_name()

        if description is None:
            description = "Generated automatically."

        return self.api.create(env['id'], name, description, limit, cvId)


    def delete(self, org, akId):
        return self.api.delete(org['label'], akId)


    def activation_key(self, org, akId):
        return self.api.activation_key(org['label'], akId)


    def add_pool(self, org, akId, poolId):
        return self.api.add_pool(org['label'], akId, poolId)


    def has_pool(self, org, akId, poolId):
        ak = self.activation_key(org, akId)

        pools = ak['pools']

        return poolId in [pool['id'] for pool in pools]


    def remove_pool(self, org, akId, poolId):
        return self.api.remove_pool(org['label'], akId, poolId)


    def add_system_group(self, org, akId, sgId):
        return self.api.add_pool(org['label'], akId, sgId)


    def remove_system_group(self, org, akId, sgId):
        return self.api.remove_pool(org['label'], akId, sgId)
