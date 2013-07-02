from common import *

import datetime
import json

import sys
import time

try:
    from katello.client.api.product import ProductAPI    
except ImportError, e:
    print "Please install Katello CLI package."
    sys.exit(-1)


class Product():
    api = ProductAPI()
    
    def create_product(self, prv, name=None, label=None, description='Built by API', gpgkey=None):

        if name is None:
            name = generate_name(8)

        if label is None:
            label = "label-%s" % name.lower()

        return self.api.create(prv['id'], name, label, description, gpgkey)


    def delete_product(self, org, pId):
        return self.api.delete(org['label'], pId)

    
    def product(self, org, pId):
        return self.api.show(org['label'], pId)


    def products_by_org(self, org, name=None):
        return self.api.products_by_org(org['label'], name)


    def sync(self, org, pId):
        task = self.api.sync(org['label'], pId)

        while task['sync_status'] != 'finished':
            task = self.api.last_sync_status(org['label'], pId)

        return task
