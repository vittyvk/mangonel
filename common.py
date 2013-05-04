import json
import random
import string
import uuid
import time

facts = json.load(open('base.json'))

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
    
def generate_system(name=None):

    if name is None:
        name = "%s.example.com" % generate_name()

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
                facts[key] = generate_name()
            elif attr_type == 'date':
                facts[key] = time.strftime('%m/%d/%Y', time.gmtime(time.time() - random.randrange(0, 100000, 1)))
    			
    for attr in copies:
        source = facts[attr]['copy']
        facts[attr] = facts[source]

    system = {
        'name'            : facts['network.hostname'],
        'cp_type'         : 'system',
        'organization_id' : None,
        'environment_id'  : None,
        'facts'           : facts,
        }
	
    return system
