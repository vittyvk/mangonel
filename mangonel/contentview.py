from common import *

import datetime
import json
import requests
import sys
import time

try:
    from katello.client.api.task_status import TaskStatusAPI
    from katello.client.api.content_view import ContentViewAPI
except ImportError, e:
    print "Please install Katello CLI package."
    sys.exit(-1)


class ContentView():
    task_api = TaskStatusAPI()
    api = ContentViewAPI()


    def delete(self, org, cvId):
        return self.api.delete(org['label'], cvId)

    
    def content_view(self, org, cvId, env):
        return self.api.show(org['label'], cvId, env['id'])


    def content_views_by_org(self, org, env=None):
        return self.api.content_views_by_org(org['label'], env)


    def content_views_by_label_name_or_id(self, org, label=None, name=None, cvId=None):
        return self.api.views_by_label_name_or_id(org['label'], label, name, cvId)[0]

    def refresh(self, cvId):

        ptask = self.api.refresh(cvId)

        task = self.task_api.status(ptask['uuid'])
        while task['state'] != 'finished':
            print "Publishing content view description %s" % name
            task = self.task_api.status(ptask['uuid'])
