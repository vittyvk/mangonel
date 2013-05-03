from common import *
import json
import requests
import sys
import time

"""
api = "<SERVER>/katello/api"

s = requests.Session()
s.auth = ("admin", "admin")
s.verify = False

r = s.get(api)

if not r.status_code == 200: sys.exit(-1)
"""


def get_org(org_name, session):
    result = None
    
    orgs = url_get(session, "organizations")

    if orgs:
        org = [org for org in orgs if org['name'] == org_name]

        if org:
            result = org[0]

    return result

def get_org_environments(org, env_name, session):
    result = None
    
    envs = url_get(session, "organizations/%s/environments" % org['label'])

    if envs:
        env = [env for env in envs if env['name'] == env_name]

        if env:
            result = env[0]

    return result


def url_get(session, url, timing=True):
    result = None

    # Strip leading forward slashes
    if url.startswith("/"): url = url[1:]
    
    r = session.get("%s/%s" % (api, url))
    if r.status_code == 200:
        result = r.json()

    return result


def url_post(session, url, payload, timing=True):
    result = None

    # Strip leading forward slashes
    if url.startswith("/"): url = url[1:]

    headers = {'content-type': 'application/json'}

    r = session.post("%s/%s" % (api, url),
                     data=json.dumps(payload),
                     headers=headers)
    if r.status_code == 200:
        result = r.json()

    return result


def add_system(org, env_name, session):
    result = None

    env = get_org_environments(org, env_name, session)
    sys_uuid = 
    system = generate_system()

    system['organization_id'] = org['label']
    system['environment_id'] = env['id']

    r = url_post(session, "%s/systems" % api, system)
