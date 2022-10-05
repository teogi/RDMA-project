FROM ubuntu:16.04

MAINTAINER teogi

RUN apt-get update

RUN apt-get install -y iptables iputils-ping net-tools iproute2 tcpdump vim sudo
RUN apt-get install -y isc-dhcp-server isc-dhcp-client
RUN apt-get install -y python python-pip wget
RUN apt-get install -y wondershaper iperf3
#RUN apt-get install -y openvswitch-switch openvswitch-common 
RUN apt-get install -y --no-install-recommends gcc make && rm -rf /avr/lib/apt/lists/*
RUN pip install six
RUN wget https://www.openvswitch.org/releases/openvswitch-2.11.4.tar.gz
RUN tar zxf openvswitch-2.11.4.tar.gz
RUN cd openvswitch-2.11.4 && ./configure --prefix=/usr --localstatedir=/var--sysconfdir=/etc \
	&& make && make install
