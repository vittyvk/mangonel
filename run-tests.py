#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

import argparse
import os
import subprocess
import sys

# Borrowed from https://github.com/pulp/pulp/blob/master/run-tests.py
# Find and eradicate any existing .pyc files, so they do not eradicate us!
PROJECT_DIR = os.path.dirname(__file__)
subprocess.call(['find', PROJECT_DIR, '-name', '*.pyc', '-delete'])

PACKAGES = [
        'activationkey_key',
        'changeset',
        'content_view_definition',
        'user',
        'organization',
        'repo',
        'system',
        'system_group',
        ]

TESTS = [
    'test_ActivationKeys',
    'test_Organizations',
    'test_SystemGroups',
    'test_Systems',
    'test_Users',
    ]

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--host', type=str, dest='host', help='Server url')
parser.add_argument('-u', '--username', type=str, dest='username', default='admin', help='Valid system username')
parser.add_argument('-p', '--password', type=str, dest='password', default='admin', help='Valid system user password')
parser.add_argument('--project', type=str, dest='project', default='/katello', help='Project can be either "katello" or "headpin"')
parser.add_argument('--port', type=str, dest='port', default='443', help='Server port, defaults to 443')

[args, ignored_args] = parser.parse_known_args()

os.environ['KATELLO_HOST'] = args.host
os.environ['KATELLO_USERNAME'] = args.username
os.environ['KATELLO_PASSWORD'] = args.password
os.environ['PROJECT'] = args.project
os.environ['KATELLO_PORT'] = args.port

env = os.environ.copy()

params = [
        'nosetests',
        '--with-xunit',
        '--with-coverage',
        '--cover-html',
        '--cover-erase',
        '--cover-package',
        ",".join(["katello.client.api.%s" % x for x in PACKAGES]),
        "--tests",
        ",".join(["tests.%s" % x for x in TESTS]),
        ]

subprocess.call(params, env=env)
