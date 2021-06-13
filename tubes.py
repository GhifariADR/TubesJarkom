from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import CPULimitedHost
from mininet.util import pmonitor
from signal import SIGINT 
import time
import os

class MyTopo( Topo):
	def __init__(self, **opts):
		Topo.__init__(self, **opts)
		
		# add host
		hostA = self.addHost('hostA')
		hostB = self.addHost('hostB')
		
		# add router
		r1 = self.addHost('r1')
		r2 = self.addHost('r2')
		r3 = self.addHost('r3')
		r4 = self.addHost('r4')
		
		# add link	
		self.addLink(hostA, r1, intfName1='ha-eth0', intfName2='r1-eth0', bw = 1)
		self.addLink(hostA, r2, intfName1='ha-eth1', intfName2='r2-eth0', bw = 1)
		self.addLink(hostB, r3, intfName1='hb-eth0', intfName2='r3-eth2', bw = 1)
		self.addLink(hostB, r4, intfName1='hb-eth1', intfName2='r4-eth0', bw = 1)
		self.addLink(r1, r4, intfName1='r1-eth2', intfName2='r4-eth2',bw = 1)
		self.addLink(r1, r3, intfName1='r1-eth1', intfName2='r3-eth0' ,bw = 0.5)
		self.addLink(r2, r3, intfName1='r2-eth1', intfName2='r3-eth1',bw = 1)
		self.addLink(r2, r4, intfName1='r2-eth2', intfName2='r4-eth1',bw = 0.5) 
def runTopo():
	os.system('mn -c')
	net = Mininet(topo=MyTopo(), link=TCLink)
	net.start()
	
	ha, hb, r1, r2, r3, r4 = net.get('hostA', 'hostB', 'r1', 'r2', 'r3', 'r4')
	
	# add ip host
	ha.cmd( 'ip addr add 192.168.1.1/24 brd + dev ha-eth0' )
	ha.cmd( 'ip addr add 192.168.2.1/24 brd + dev ha-eth1' )
	
	hb.cmd( 'ip addr add 192.168.3.1/24 brd + dev hb-eth0' )
	hb.cmd( 'ip addr add 192.168.4.1/24 brd + dev hb-eth1' )
		
	# add ip for router
	r1.cmd( 'ip addr add 192.168.1.2/24 brd + dev r1-eth0' )
	r1.cmd( 'ip addr add 192.168.5.1/24 brd + dev r1-eth1' )
	r1.cmd( 'ip addr add 192.168.5.9/24 brd + dev r1-eth2' )
	
	r2.cmd( 'ip addr add 192.168.2.2/24 brd + dev r2-eth0' )
	r2.cmd( 'ip addr add 192.168.5.17/24 brd + dev r2-eth1' )
	r2.cmd( 'ip addr add 192.168.5.25/24 brd + dev r2-eth2' )
		
	r3.cmd( 'ip addr add 192.168.5.18/24 brd + dev r3-eth0' )
	r3.cmd( 'ip addr add 192.168.3.2/24 brd + dev r3-eth1' )
	r3.cmd( 'ip addr add 192.168.5.2/24 brd + dev r3-eth2' )
		
	r4.cmd( 'ip addr add 192.168.4.2/24 brd + dev r4-eth0' )
	r4.cmd( 'ip addr add 192.168.5.26/24 brd + dev r4-eth1' )
	r4.cmd( 'ip addr add 192.168.5.10/24 brd + dev r4-eth2' )
		
	# start IP
	r1.cmd( 'sysctl net.ipv4.ip_forward=1' )
	r2.cmd( 'sysctl net.ipv4.ip_forward=1' )
	r3.cmd( 'sysctl net.ipv4.ip_forward=1' )
	r4.cmd( 'sysctl net.ipv4.ip_forward=1' )
		
	# statik routing Host
	ha.cmd("ip rule add from 192.168.1.1 table 1")
	ha.cmd("ip rule add from 192.168.2.1 table 2")
	ha.cmd("ip route add 192.168.1.0/24 dev ha-eth0 scope link table 1")
	ha.cmd("ip route add default via 192.168.1.2 dev ha-eth0 table 1")
	ha.cmd("ip route add 192.168.2.0/24 dev ha-eth1 scope link table 2")
	ha.cmd("ip route add default via 192.168.2.2 dev ha-eth1 table 2")
	ha.cmd("ip route add default scope global nexthop via 192.168.1.2 dev ha-eth0")
		
	hb.cmd("ip rule add from 192.168.3.1 table 3")
	hb.cmd("ip rule add from 192.168.4.1 table 4")
	hb.cmd("ip route add 192.168.3.0/24 dev hb-eth0 scope link table 3")
	hb.cmd("ip route add default via 192.168.3.2 dev hb-eth0 table 3")
	hb.cmd("ip route add 192.168.4.0/24 dev hb-eth1 scope link table 4")
	hb.cmd("ip route add default via 192.168.4.2 dev hb-eth1 table 4")
	hb.cmd("ip route add default scope global nexthop via 192.168.3.2 dev hb-eth0")
	
	# statik routing router
	r1.cmd("route add -net 192.168.5.16/24 gw 192.168.5.2")
	r1.cmd("route add -net 192.168.2.0/24 gw 192.168.5.2")
	r1.cmd("route add -net 192.168.4.0/24 gw 192.168.5.10")
	r1.cmd("route add -net 192.168.3.0/24 gw 192.168.5.2")
	r1.cmd("route add -net 192.168.5.24/24 gw 192.168.5.10")
	
	r2.cmd("route add -net 192.168.1.0/24 gw 192.168.5.18")
	r2.cmd("route add -net 192.168.5.0/24 gw 192.168.5.18")
	r2.cmd("route add -net 192.168.3.0/24 gw 192.168.5.18")
	r2.cmd("route add -net 192.168.4.0/24 gw 192.168.5.26")
	r2.cmd("route add -net 192.168.5.0/24 gw 192.168.5.26")
	
	r3.cmd("route add -net 192.168.5.0/24 gw 192.168.5.2")
	r3.cmd("route add -net 192.168.2.0/24 gw 192.168.5.25")
	r3.cmd("route add -net 192.168.4.0/24 gw 192.168.5.25")
	r3.cmd("route add -net 192.168.1.0/24 gw 192.168.5.1")
	#r3.cmd("route add -net 192.168.5.16/24 gw 192.168.5.2")
	
	r4.cmd("route add -net 192.168.2.0/24 gw 192.168.5.25")
	r4.cmd("route add -net 192.168.1.0/24 gw 192.168.5.9")
	r4.cmd("route add -net 192.168.3.0/24 gw 192.168.5.9")
	#r4.cmd("route add -net 192.168.5.16/24 gw 192.168.5.2")
	#r4.cmd("route add -net 192.168.5.16/24 gw 192.168.5.2")	
		
		
	CLI(net)
	net.stop()
	
if __name__=='__main__':
	runTopo()
	setLogLevel( 'info' )
	
topos = { 'myTopo': (lambda: MyTopo() ) }		
		
	
