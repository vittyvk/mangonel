import json
import random
import string
import uuid

facts = json.load(open('base.json'))

def generate_uuid():

    uuid_obj = uuid.uuid1()

    return uuid_obj.urn.split(":")[-1]


def random_name(min=4, max=8):

    if min <= 0:
        min = 4
    if max < min:
        max = min
        
    r = random.SystemRandom()
    pool = string.ascii_letters + string.digits

    return str().join(r.choice(pool) for x in range(random.randint(min, max)))


def random_ipaddr():

    ipaddr = ".".join(str(random.randrange(0, 255, 1)) for x in range(4))

    return ipaddr
    
def generate_system(name=None):

    if name is None:
        name = "%s.example.com" % random_name()

    uuid = generate_uuid()
    ipaddr = random_ipaddr()
    
    system = {
        'name'            : name,
        'cp_type'         : 'system',
        'organization_id' : None,
        'environment_id'  : None,
        'facts'           : facts,
        }

    system['facts']['dmi.system.uuid'] = uuid
    system['facts']['net.interface.eth1.ipaddr'] = ipaddr
    system['facts']['network.hostname'] = name
    system['facts']['network.ipaddr']
    system['facts']['uname.nodename'] = name
    system['facts']['virt.uuid'] = uuid

    return system
