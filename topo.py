from mininet.topo import Topo
from mininet.node import Node
import sys

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class MyTopology(Topo):
    def __init__(self, admins=2, workers=2):
        # Initialize topology
        Topo.__init__(self)

        ip_addresses = { 'DMZ': '192.168.1.{}/24', 
                         'admins': '192.168.2.{}/24',
                         'workers': '192.168.3.{}/24',
                         'server': '192.168.4.{}/24' }

        hosts_names = { 'DMZ': 'hd{}', 
                        'admins': 'ha{}',
                        'workers': 'hw{}',
                        'server': 'hs{}' }

        # Routers from the network
        internal_router = self.addNode('r1', cls=LinuxRouter, ip='192.168.1.1/24')

        # External host used as an attacker
        external_host = self.addHost('attacker',
                                     ip='200.0.0.2/24',
                                     defaultRoute='via 200.0.0.1')

        external_switch = self.addSwitch('se1')


        # Switches from the network
        switches = { 'DMZ': self.addSwitch('s1'),
                     'admins': self.addSwitch('s2'),
                     'workers': self.addSwitch('s3'),
                     'server': self.addSwitch('s4') }
            

        # Add admins host to the network
        host_number = 1
        for admin in range(admins):
            name = hosts_names['admins'].format(host_number)
            ip_address = ip_addresses['admins'].format(host_number + 1)
            host = self.addHost(name, ip=ip_address, defaultRoute='via 192.168.2.1')
            host_number += 1
            self.addLink(switches['admins'], host)

        # Add workers host to the network
        host_number = 1
        for worker in range(workers):
            name = hosts_names['workers'].format(host_number)
            ip_address = ip_addresses['workers'].format(host_number + 1)
            host = self.addHost(name, ip=ip_address, defaultRoute='via 192.168.3.1')
            host_number += 1
            self.addLink(switches['workers'], host)


        server = self.addHost(hosts_names['server'].format(1),
                              ip='192.168.4.2/24',
                              defaultRoute='via 192.168.4.1')

        web = self.addHost(hosts_names['DMZ'].format(1),
                           ip='192.168.1.3/24',
                           defaultRoute='via 192.168.1.1')

        self.addLink(switches['DMZ'], web)
        self.addLink(switches['server'], server)
        self.addLink(external_switch, external_host)

        self.addLink( switches['DMZ'], internal_router, intfName2='r1-eth1',
                      params2={ 'ip' : '192.168.1.1/24' } )
        self.addLink( switches['admins'], internal_router, intfName2='r1-eth2',
                      params2={ 'ip' : '192.168.2.1/24' } )
        self.addLink( switches['workers'], internal_router, intfName2='r1-eth3',
                      params2={ 'ip' : '192.168.3.1/24' } )
        self.addLink( switches['server'], internal_router, intfName2='r1-eth4',
                      params2={ 'ip' : '192.168.4.1/24' } )
        self.addLink( external_switch, internal_router, intfName2='r1-eth5',
                      params2={ 'ip' : '200.0.0.1/24' } )





topos = {'topo': (lambda admins=2, workers=2: MyTopology(admins=admins, workers=workers))}
