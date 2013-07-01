import json
import logging
import os
import random
import string
import uuid
import time

from threading import Thread
from Queue import Queue


logger = logging.getLogger("mangonel")

facts = json.load(open(os.path.join(os.path.dirname(__file__), 'base.json')))
packages = json.load(open(os.path.join(os.path.dirname(__file__), 'packages.json')))

REQUEST_DELAY = 10
MAX_ATTEMPTS = 720

def queued_work(worker_method, org, env, max_systems, num_threads):
    def worker():
         while True:
             size = q.qsize()
             if (size % num_threads) == 0 and size != 0:
                 logger.debug("%s items left to process" % size)
             item = q.get()
             try:
                 return_list.append(worker_method(org, env))
             except Exception, e:
                logger.debug("Exception from worker: %s" % e)

             q.task_done()

    q = Queue()
    return_list = []

    for i in range(num_threads):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    for i in range(0, max_systems):
        q.put(org, env)

    q.join()

    logger.debug("queue work is complete, returning %s items" % len(return_list))

    return return_list

def generate_uuid():

    uuid_obj = uuid.uuid1()

    return uuid_obj.urn.split(":")[-1]


def generate_name(min=4, max=8):

    if min <= 0:
        min = 4
    if max < min:
        max = min

    r = random.SystemRandom()
    pool1 = string.ascii_lowercase
    pool2 = string.digits

    return "%s-%s" % (
        str().join(r.choice(pool1) for x in range(random.randint(min, max))),
        str().join(r.choice(pool2) for x in range(random.randint(min, max)))
        )


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
