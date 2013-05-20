import json
import os
import random
import string
import uuid
import time

facts = json.load(open(os.path.join(os.path.dirname(__file__), 'base.json')))
packages = json.load(open(os.path.join(os.path.dirname(__file__), 'packages.json')))

def generate_uuid():

    uuid_obj = uuid.uuid1()

    return uuid_obj.urn.split(":")[-1]


def generate_name(min=4, max=8):

    if min <= 0:
        min = 4
    if max < min:
        max = min

    r = random.SystemRandom()
    pool = string.ascii_letters + string.digits

    return str().join(r.choice(pool) for x in range(random.randint(min, max)))


def generate_ipaddr():

    ipaddr = ".".join(str(random.randrange(0, 255, 1)) for x in range(4))

    return ipaddr

def generate_mac():
    chars = ['a','b','c','d','e','f','0','1','2','3','4','5','6','7','8','9']
    mac = ":".join(chars[random.randrange(0, len(chars), 1)]+chars[random.randrange(0, len(chars), 1)] for x in range(6))

    return mac

def generate_facts(system_name):

    uuid = generate_uuid()
    ipaddr = generate_ipaddr()

    copies = {}

    for key in facts:
        if type(facts[key]) == dict:
            attr_type = facts[key].keys()[0]
            if attr_type == 'array':
                elem = random.randrange(0, len(facts[key]['array']), 1)
                facts[key] = facts[key]['array'][elem]
            elif attr_type == 'uuid':
                facts[key] = generate_uuid()
            elif attr_type == 'copy':
                copies[key] = facts[key]['copy']
            elif attr_type == 'ipaddr':
                facts[key] = generate_ipaddr()
            elif attr_type == 'hostname':
                facts[key] = system_name
            elif attr_type == 'date':
                facts[key] = time.strftime('%m/%d/%Y', time.gmtime(time.time() - random.randrange(0, 100000, 1)))
            elif attr_type == 'macaddr':
                facts[key] = generate_mac()

    for attr in copies:
        source = facts[attr]['copy']
        facts[attr] = facts[source]

    return facts

def packages_list():
    return packages
