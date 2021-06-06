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
	def__init__(self,**opts):
		Topo.__init__(self,**opts):
		ha = self.addHost('ha', ip='192.168.0.1/24', mac='13:01:19:40:34:00:00:01')
		hb = self.addHost('hb', ip='192.168.0.2/24', mac='13:01:19:40:34:00:00:02')
		
	
		r1 = self.addHost('r1', ip='192.168.1.1/29',)
		r2 = self.addHost('r2', ip='192.168.2.1/29',)
		r3 = self.addHost('r3', ip='192.168.3.1/29',)
		r4 = self.addHost('r4', ip='192.168.4.1/29',)
	
		self.addLink(ha, r1, cls=TCPLink, bw = 1)
		self.addLink(ha, r2, cls=TCPLink, bw = 1)
		self.addLink(hb, r3, cls=TCPLink, bw = 1)
		self.addLink(hb, r4, cls=TCPLink, bw = 1)
		self.addLink(r1, r4, bw = 1)
		self.addLink(r1, r3, bw = 0.5)
		self.addLink(r2, r3, bw = 1)
		self.addLink(r2, r4, bw = 0.5) 
		
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
		
	
