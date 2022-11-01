#! /usr/bin/python
import time
from argparse import ArgumentParser as Parser
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, Switch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.util import dumpNodeConnections

class Topology():
    def __init__(self, opts):
        
        #initialize topology
        net = Mininet(link = TCLink)
 
        # add hosts and switch
        A = net.addHost("A")
        B = net.addSwitch("B1",failMode = 'standalone')
        C = net.addHost("C")
        APr = net.addHost("APr")
        sink = net.addHost("sink")
        
        # add bandwidth-limited links
        if opts.bw:
            bw=int(opts.bw)
            print('bandwidth is %d' % (bw))
            bandwidthControl(net,bw)
        else:
            net.addLink('A'   ,'B1')
            net.addLink('C'   ,'B1')
            net.addLink('APr' ,'B1')
            
        net.addLink('sink','B1') # sink is unlimited

        # set member variables
        self.net = net
        self.A = A
        self.B = B
        self.C = C
        self.APr = APr
        self.sink = sink
        
def bandwidthControl(net,Bw):
        net.addLink('A'   ,'B1',bw=Bw)
        net.addLink('C'   ,'B1',bw=Bw)
        net.addLink('APr' ,'B1',bw=Bw)


if __name__ == '__main__':
    parser = Parser()
    parser.add_argument("-b","--bandwidth",dest='bw')
    arg = parser.parse_args()
    tp = Topology(arg)
    tp.net.start()
    tp.net.startTerms()
    CLI(tp.net)
    tp.net.stop() 
