from common import *

import datetime
import json
import sys
import time

try:
    from katello.client.api.task_status import TaskStatusAPI
    from katello.client.api.content_view import ContentViewAPI
except ImportError, e:
    print "Please install Katello CLI package."
    sys.exit(-1)


class ContentView(ContentViewAPI):
    task_api = TaskStatusAPI()

    def __init__(self):
        super(ContentView, self).__init__()

    def delete(self, org, cvId):
        return super(ContentView, self).delete(org['label'], cvId)

    def content_view(self, org, cvId, envId=None):
        return super(ContentView, self).show(org['label'], cvId, envId)

    def content_views_by_org(self, org, env=None):
        return super(ContentView, self).content_views_by_org(org['label'], env)


    def content_views_by_label_name_or_id(self, org, label=None, name=None, cvId=None):
        return super(ContentView, self).views_by_label_name_or_id(org['label'], label, name, cvId)[0]


    def refresh(self, cvId):

        ptask = super(ContentView, self).refresh(cvId)

        task = self.task_api.status(ptask['uuid'])
        while task['state'] != 'finished':
            print "Publishing content view description %s" % name
            task = self.task_api.status(ptask['uuid'])
