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


class Product(ProductAPI):

    def __init__(self):
        super(Product, self).__init__()

    def create(self, prv, name=None, label=None, description='Built by API', gpgkey=None):

        if name is None:
            name = generate_name(8)

        if label is None:
            label = "label-%s" % name.lower()

        return super(Product, self).create(prv['id'], name, label, description, gpgkey)

    def delete(self, org, pId):
        return super(Product, self).delete(org['label'], pId)

    def product(self, org, pId):
        return super(Product, self).show(org['label'], pId)

    def products_by_org(self, org, name=None):
        return super(Product, self).products_by_org(org['label'], name)

    def sync(self, org, pId):
        task = super(Product, self).sync(org['label'], pId)

        while task['sync_status'] != 'finished':
            task = super(Product, self).last_sync_status(org['label'], pId)

        return task
