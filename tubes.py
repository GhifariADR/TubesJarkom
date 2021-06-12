from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import CPULimitedHost
import time
import os

class MyTopo(Topo):
	net = Mininet( link=TCLink )
		
		ha = net.addHost('ha', ip='192.168.0.1/30')
		hb = net.addHost('hb', ip='192.168.0.2/30')
		
	
		r1 = net.addHost('r1', ip='192.168.1.1/30',)
		r2 = net.addHost('r2', ip='192.168.2.1/30',)
		r3 = net.addHost('r3', ip='192.168.3.1/30',)
		r4 = net.addHost('r4', ip='192.168.4.1/30',)
	
		net.addLink(ha, r1, cls=TCPLink, intfName1='ha-eth0', intfName2='r1-eth0', bw = 1)
		net.addLink(ha, r2, cls=TCPLink, intfName1='ha-eth1', intfName2='r2-eth0', bw = 1)
		net.addLink(hb, r3, cls=TCPLink, intfName1='hb-eth0', intfName2='r3-eth2', bw = 1)
		net.addLink(hb, r4, cls=TCPLink, intfName1='hb-eth1', intfName2='r4-eth0', bw = 1)
		net.addLink(r1, r4, intfName1='r1-eth2', intfName2='r4-eth2',bw = 1)
		net.addLink(r1, r3, intfName1='r1-eth1', intfName2='r3-eth0' ,bw = 0.5)
		net.addLink(r2, r3, intfName1='r2-eth1', intfName2='r3-eth1',bw = 1)
		net.addLink(r2, r4, intfName1='r2-eth2', intfName2='r4-eth1',bw = 0.5) 
		
		ha.cmd( 'ip addr add 192.168.0.1/30 brd + dev ha-eth0' )
		ha.cmd( 'ip addr add 192.168.3.1/30 brd + dev ha-eth1' )
		
		hb.cmd( 'ip addr add 192.168.4.1/30 brd + dev hb-eth0' )
		hb.cmd( 'ip addr add 192.168.5.1/30 brd + dev hb-eth1' )
		
		r1.cmd( 'ip addr add 192.168.0.2/30 brd + dev r1-eth0' )
		r1.cmd( 'ip addr add 192.168.1.1/30 brd + dev r1-eth1' )
		r1.cmd( 'ip addr add 192.168.7.1/30 brd + dev r1-eth2' )
		
		r2.cmd( 'ip addr add 192.168.3.2/30 brd + dev r2-eth0' )
		r2.cmd( 'ip addr add 192.168.2.1/30 brd + dev r2-eth1' )
		r2.cmd( 'ip addr add 192.168.6.1/30 brd + dev r2-eth2' )
		
		r3.cmd( 'ip addr add 192.168.1.2/30 brd + dev r3-eth0' )
		r3.cmd( 'ip addr add 192.168.2.2/30 brd + dev r3-eth1' )
		r3.cmd( 'ip addr add 192.168.4.2/30 brd + dev r3-eth2' )
		
		r4.cmd( 'ip addr add 192.168.5.2/30 brd + dev r4-eth0' )
		r4.cmd( 'ip addr add 192.168.6.2/30 brd + dev r4-eth1' )
		r4.cmd( 'ip addr add 192.168.7.2/30 brd + dev r4-eth2' )
		
		r1.cmd( 'sysctl net.ipv4.ip_forward=1' )
		r2.cmd( 'sysctl net.ipv4.ip_forward=1' )
		r3.cmd( 'sysctl net.ipv4.ip_forward=1' )
		r4.cmd( 'sysctl net.ipv4.ip_forward=1' )
		
		
		
		
def runTopo():
	os.system('mn -cc')
		
	topo = Mytopo()
	net = Mininet(topo=topo, host=CPULimitedhost, link=TCLink)
	net.start()
    
		
	time.sleep(15)
		
	ha.cmdPrint('fg')
	CLI(net)
	net.stop()
	
if __name__=='__main__':
	setLogLevel('info')
	runTopo()
		
topos = { 'mytopo' : (lamda: Mytopo() ) }		
		
	
