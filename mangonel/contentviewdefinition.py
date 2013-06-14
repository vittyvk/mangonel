from common import *

import datetime
import json
import requests
import sys
import time

try:
    from katello.client.api.task_status import TaskStatusAPI
    from katello.client.api.content_view_definition import ContentViewDefinitionAPI
except ImportError, e:
    print "Please install Katello CLI package."
    sys.exit(-1)


class ContentViewDefinition():
    task_api = TaskStatusAPI()
    api = ContentViewDefinitionAPI()
    
    def create_content_view_definition(self, org, name=None, label=None, description=None, composite=False):

        if name is None:
            name = generate_name(8)


        if label is None:
            label = "label-%s" % name.lower()

        if description is None:
            description = "Created on %s" % datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            
        return self.api.create(org['label'], name, label, description, composite)


    def delete_content_view_definition(self, cvdId):
        return self.api.delete(cvdId)

    
    def content_view_definition(self, org, cvdId):
        return self.api.show(org['label'], cvdId)


    def content_view_definitions_by_org(self, org):
        return self.api.content_view_definitions_by_org(org['label'])


    def publish(self, org, cvdId, name=None, label=None, description=None):
        
        if name is None:
            name = generate_name(8)


        if label is None:
            label = "label-%s" % name.lower()

        if description is None:
            description = "Published on %s" % datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        ptask = self.api.publish(org['label'], cvdId, name, label, description)

        task = self.task_api.status(ptask['uuid'])
        while task['state'] != 'finished':
            print "Publishing content view description %s" % name
            task = self.task_api.status(ptask['uuid'])

    
    def clone(self, org, cvdId, name=None, label=None, description=None):
        
        if name is None:
            name = generate_name(8)


        if label is None:
            label = "label-%s" % name.lower()

        if description is None:
            description = "Cloned on %s" % datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            
        return self.api.clone(org['label'], cvdId, name, label, description)

    
    def update_products(self, org, cvdId, prd):
        return self.api.update_products(org['label'], cvdId, [prd['id']])


    def products(self, org, cvdId):
        return self.api.products(org['label'], cvdId)
