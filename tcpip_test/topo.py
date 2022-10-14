#! /usr/bin/python
import time
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, Switch
from mininet.cli import CLI

def topology():
    net = Mininet()

    # add nodes and links
    A = net.addHost("A")
    B = net.addSwitch("B1",failMode = 'standalone')
    C = net.addHost("C")
    APr = net.addHost("APr")
    sink = net.addHost("sink")
    
    net.addLink('A','B1')
    net.addLink('C','B1')
    net.addLink('APr','B1')
    net.addLink('sink','B1')

    net.start()
    
    CLI(net)
    net.stop()

#def bandwidthControl():


if __name__ == '__main__':
    net = topology()
