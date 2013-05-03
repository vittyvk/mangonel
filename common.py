import random
import string
import uuid

facts = {
    'cpu.core(s)_per_socket': '1',
     'cpu.cpu(s)': '1',
     'cpu.cpu_socket(s)': '1',
     'distribution.id': 'Santiago',
     'distribution.name': 'Red Hat Enterprise Linux Server',
     'distribution.version': '6.2',
     'dmi.bios.address': '0xe8000',
     'dmi.bios.bios_revision': '1.0',
     'dmi.bios.relase_date': '01/01/2007',
     'dmi.bios.rom_size': '64 KB',
     'dmi.bios.runtime_size': '96 KB',
     'dmi.bios.vendor': 'Seabios',
     'dmi.bios.version': '0.5.1',
     'dmi.chassis.asset_tag': 'Not Specified',
     'dmi.chassis.boot-up_state': 'Safe',
     'dmi.chassis.lock': 'Not Present',
     'dmi.chassis.manufacturer': 'Red Hat',
     'dmi.chassis.power_supply_state': 'Safe',
     'dmi.chassis.security_status': 'Unknown',
     'dmi.chassis.serial_number': 'Not Specified',
     'dmi.chassis.thermal_state': 'Safe',
     'dmi.chassis.type': 'Other',
     'dmi.chassis.version': 'Not Specified',
     'dmi.memory.array_handle': '0x1000',
     'dmi.memory.bank_locator': 'Not Specified',
     'dmi.memory.data_width': '64 bit',
     'dmi.memory.error_correction_type': 'Multi-bit ECC',
     'dmi.memory.error_information_handle': 'Not Provided',
     'dmi.memory.form_factor': 'DIMM',
     'dmi.memory.location': 'Other',
     'dmi.memory.locator': 'DIMM 0',
     'dmi.memory.maximum_capacity': '2 GB',
     'dmi.memory.size': '2048 MB',
     'dmi.memory.speed': '  (ns)',
     'dmi.memory.total_width': '64 bit',
     'dmi.memory.type': 'RAM',
     'dmi.memory.use': 'System Memory',
     'dmi.processor.family': 'Other',
     'dmi.processor.socket_designation': 'CPU 1',
     'dmi.processor.status': 'Populated:Enabled',
     'dmi.processor.type': 'Central Processor',
     'dmi.processor.upgrade': 'Other',
     'dmi.processor.version': 'Not Specified',
     'dmi.processor.voltage': ' ',
     'dmi.system.family': 'Red Hat Enterprise Linux',
     'dmi.system.manufacturer': 'Red Hat',
     'dmi.system.product_name': 'KVM',
     'dmi.system.serial_number': 'Not Specified',
     'dmi.system.sku_number': 'Not Specified',
     'dmi.system.status': 'No errors detected',
     'dmi.system.uuid': None,
     'dmi.system.version': 'RHEL 6.2.0 PC',
     'dmi.system.wake-up_type': 'Power Switch',
     'lscpu.architecture': 'x86_64',
     'lscpu.bogomips': '4200.01',
     'lscpu.byte_order': 'Little Endian',
     'lscpu.core(s)_per_socket': '1',
     'lscpu.cpu(s)': '1',
     'lscpu.cpu_family': '6',
     'lscpu.cpu_mhz': '2100.008',
     'lscpu.cpu_op-mode(s)': '32-bit, 64-bit',
     'lscpu.cpu_socket(s)': '1',
     'lscpu.hypervisor_vendor': 'KVM',
     'lscpu.l1d_cache': '64K',
     'lscpu.l1i_cache': '64K',
     'lscpu.l2_cache': '512K',
     'lscpu.model': '13',
     'lscpu.numa_node(s)': '1',
     'lscpu.numa_node0_cpu(s)': '0',
     'lscpu.on-line_cpu(s)_list': '0',
     'lscpu.stepping': '3',
     'lscpu.thread(s)_per_core': '1',
     'lscpu.vendor_id': 'AuthenticAMD',
     'lscpu.virtualization_type': 'full',
     'memory.memtotal': '2055092',
     'memory.swaptotal': '2064376',
     'net.interface.eth1.broadcast': '10.10.169.255',
     'net.interface.eth1.hwaddr': '52:54:00:b5:30:24',
     'net.interface.eth1.ipaddr': None,
     'net.interface.eth1.netmask': '255.255.254.0',
     'net.interface.lo.broadcast': '0.0.0.0',
     'net.interface.lo.hwaddr': '00:00:00:00:00:00',
     'net.interface.lo.ipaddr': '127.0.0.1',
     'net.interface.lo.netmask': '255.0.0.0',
     'network.hostname': None,
     'network.ipaddr': None,
     'system.entitlements_valid': 'false',
     'uname.machine': 'x86_64',
     'uname.nodename': None,
     'uname.release': '2.6.32-220.el6.x86_64',
     'uname.sysname': 'Linux',
     'uname.version': '#1 SMP Wed Nov 9 08:03:13 EST 2011',
     'virt.host_type': 'kvm',
     'virt.is_guest': 'true',
     'virt.uuid': None,
    }


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
