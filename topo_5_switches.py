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
                         'admins': '192.168.1.{}/24',
                         'workers': '192.168.1.{}/24',
                         'server': '192.168.1.{}/24' }

        hosts_names = { 'DMZ': 'hd{}', 
                        'admins': 'ha{}',
                        'workers': 'hw{}',
                        'server': 'hs{}' }


        # Switches from the network
        switch = self.addSwitch('s1')
        switches = { "DMZ": self.addSwitch('s2'),
                     "admins": self.addSwitch('s3'),
                     "workers": self.addSwitch('s4'),
                     "server": self.addSwitch('s5') }
        self.addLink(switch, switches["DMZ"])
        self.addLink(switch, switches["admins"])
        self.addLink(switch, switches["workers"])
        self.addLink(switch, switches["server"])
            

        # Add admins host to the network
        host_number = 1
        address_number = 100
        for admin in range(admins):
            name = hosts_names['admins'].format(host_number)
            ip_address = ip_addresses['admins'].format(address_number)
            host = self.addHost(name, ip=ip_address, defaultRoute='via 192.168.1.1')
            host_number += 1
            address_number += 1
            self.addLink(switches["admins"], host)

        host_number = 1
        # Add workers host to the network
        for worker in range(workers):
            name = hosts_names['workers'].format(host_number)
            ip_address = ip_addresses['workers'].format(address_number)
            host = self.addHost(name, ip=ip_address, defaultRoute='via 192.168.1.1')
            host_number += 1
            address_number += 1
            self.addLink(switches["workers"], host)


        server = self.addHost(hosts_names['server'].format(1),
                              ip=ip_addresses['server'].format(address_number),
                              defaultRoute='via 192.168.1.1')

        address_number += 1

        web = self.addHost(hosts_names['DMZ'].format(1),
                           ip=ip_addresses['DMZ'].format(address_number),
                           defaultRoute='via 192.168.1.1')

        self.addLink(switches["DMZ"], web)
        self.addLink(switches["server"], server)


topos = {'topo': (lambda admins=2, workers=2: MyTopology(admins=admins, workers=workers))}
