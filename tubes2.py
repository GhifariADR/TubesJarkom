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

def MyTopo():
	net = Mininet( link=TCLink )
		
	# add host
	ha = net.addHost('ha', ip='192.168.0.1/24', deafultRoute = None )
	hb = net.addHost('hb', ip='192.168.4.1/24', defaultRoute = None )
		
	# add router
	r1 = net.addHost('r1', ip='192.168.0.2/24')
	r2 = net.addHost('r2', ip='192.168.3.2/24')
	r3 = net.addHost('r3', ip='192.168.4.2/24')
	r4 = net.addHost('r4', ip='192.168.5.2/24')
		
	# add link	
	net.addLink(ha, r1, intfName1='ha-eth0', intfName2='r1-eth0', bw = 1)
	net.addLink(ha, r2, intfName1='ha-eth1', intfName2='r2-eth0', bw = 1)
	net.addLink(hb, r3, intfName1='hb-eth0', intfName2='r3-eth2', bw = 1)
	net.addLink(hb, r4, intfName1='hb-eth1', intfName2='r4-eth0', bw = 1)
	net.addLink(r1, r4, intfName1='r1-eth2', intfName2='r4-eth2',bw = 1)
	net.addLink(r1, r3, intfName1='r1-eth1', intfName2='r3-eth0' ,bw = 0.5)
	net.addLink(r2, r3, intfName1='r2-eth1', intfName2='r3-eth1',bw = 1)
	net.addLink(r2, r4, intfName1='r2-eth2', intfName2='r4-eth1',bw = 0.5) 
		
	# add ip host
	ha.cmd( 'ip addr add 192.168.0.1/24 brd + dev ha-eth0' )
	ha.cmd( 'ip addr add 192.168.3.1/24 brd + dev ha-eth1' )
	
	hb.cmd( 'ip addr add 192.168.4.1/24 brd + dev hb-eth0' )
	hb.cmd( 'ip addr add 192.168.5.1/24 brd + dev hb-eth1' )
		
	# add ip for router
	r1.cmd( 'ip addr add 192.168.0.2/24 brd + dev r1-eth0' )
	r1.cmd( 'ip addr add 192.168.1.1/24 brd + dev r1-eth1' )
	r1.cmd( 'ip addr add 192.168.7.1/24 brd + dev r1-eth2' )
	
	r2.cmd( 'ip addr add 192.168.3.2/24 brd + dev r2-eth0' )
	r2.cmd( 'ip addr add 192.168.2.1/24 brd + dev r2-eth1' )
	r2.cmd( 'ip addr add 192.168.6.1/24 brd + dev r2-eth2' )
		
	r3.cmd( 'ip addr add 192.168.1.2/24 brd + dev r3-eth0' )
	r3.cmd( 'ip addr add 192.168.2.2/24 brd + dev r3-eth1' )
	r3.cmd( 'ip addr add 192.168.4.2/24 brd + dev r3-eth2' )
		
	r4.cmd( 'ip addr add 192.168.5.2/24 brd + dev r4-eth0' )
	r4.cmd( 'ip addr add 192.168.6.2/24 brd + dev r4-eth1' )
	r4.cmd( 'ip addr add 192.168.7.2/24 brd + dev r4-eth2' )
		
	# start IP
	r1.cmd( 'sysctl net.ipv4.ip_forward=1' )
	r2.cmd( 'sysctl net.ipv4.ip_forward=1' )
	r3.cmd( 'sysctl net.ipv4.ip_forward=1' )
	r4.cmd( 'sysctl net.ipv4.ip_forward=1' )
		
	# statik routing
	ha.cmd("ip rule add from 192.168.0.1 table 1")
	ha.cmd("ip rule add from 192.168.3.1 table 2")
	ha.cmd("ip route add 192.168.0.0/24 dev ha-eth0 scope link table 1")
	ha.cmd("ip route add default via 192.168.0.2 dev ha-eth0 table 1")
	ha.cmd("ip route add 192.168.3.0/24 dev ha-eth1 scope link table 2")
	ha.cmd("ip route add default via 192.168.3.2 dev ha-eth1 table 2")
	ha.cmd("ip route add default scope global nexthop via 192.168.0.2 dev ha-eth0")
		
	hb.cmd("ip rule add from 192.168.4.1 table 1")
	hb.cmd("ip rule add from 192.168.5.1 table 2")
	hb.cmd("ip route add 192.168.4.0/24 dev hb-eth0 scope link table 1")
	hb.cmd("ip route add default via 192.168.4.2 dev hb-eth0 table 1")
	hb.cmd("ip route add 192.168.5.0/24 dev hb-eth1 scope link table 2")
	hb.cmd("ip route add default via 192.168.5.2 dev hb-eth1 table 2")
	hb.cmd("ip route add default scope global nexthop via 192.168.4.2 dev hb-eth0")
		
		
	#r3.cmd('ip route add 192.168.1.0/24 via 192.168.255.9 dev r3-eth2')
    	#r1.cmd('ip route add 192.168.3.0/29 via 192.168.255.10 dev r2-eth2')
   		
  	#r4.cmd('ip route add 192.168.2.0/29 via 192.168.255.9 dev r3-eth2')
    	#r2.cmd('ip route add 192.168.3.0/29 via 192.168.255.10 dev r2-eth2')
    		
    	#r4.cmd('ip route add 192.168.2.0/29 via 192.168.255.9 dev r3-eth2')
    	#r1.cmd('ip route add 192.168.3.0/29 via 192.168.255.10 dev r2-eth2')
    		
    	#r3.cmd('ip route add 192.168.2.0/29 via 192.168.255.9 dev r3-eth2')
    	#r2.cmd('ip route add 192.168.3.0/29 via 192.168.255.10 dev r2-eth2')
		
		
		
		
	CLI(net)
	
if __name__=='__main__':
	os.system('mn -c')
	os.system( 'clear' )
	setLogLevel( 'info' )
	MyTopo()		
		
	
