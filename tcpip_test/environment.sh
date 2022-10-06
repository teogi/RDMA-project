#!/bin/bash

function check_privilege() {
	if [ "$(whoami)" != "root" ]; then
		echo "require the root privilege"
		exit -1
	fi
	return 0
}

function create_ctr() {
	local run=$(docker inspect -f {{.State.Pid}} $1 2> /dev/null)
	if [ "$run" != "" ]; then
		echo "container $1 already created,recreating..."
		docker stop $1 > /dev/null
		docker rm $1 > /dev/null
	fi
	docker run -dit --cap-add NET_ADMIN --cap-add NET_BROADCAST \
			--privileged --name $1 $2
	if [ "$?" = "0" ]; then
		echo "container $1 create successfully"
	else
		echo "Error occured"	
	fi
}

function create_link() {
	local link1="${1}${2}veth"
	local link2="${2}${1}veth"
	ip link add  $link1 type veth peer $link2
	ip link set $link1 netns $(docker inspect -f {{.State.Pid}} $1)
	ip link set $link2 netns $(docker inspect -f {{.State.Pid}} $2)
	echo "$link1 $link2 established"
	add_ip_addr $1 "192.168.0.${count}/24" $link1
	add_ip_addr $2 "192.168.0.${count}/24" $link2
}

function add_ip_addr() {
	local dev=${1}
	local addr=${2}
	local link=${3}
	docker exec $dev ip addr add "$addr" dev "$link"
	res=$?
	if [ $res -eq 0 ]; then
		echo "ip address $addr added to $link"
		count=$(($count+1))
	fi
	docker exec $dev ip link set $link up
}

function dexec() {
	docker exec $*
}

check_privilege
create_ctr A1 tcpip
create_ctr B1 tcpip
create_ctr C1 tcpip
create_ctr AP1 tcpip
create_ctr sink1 tcpip

count=1
create_link A1 B1
create_link B1 C1
create_link AP1 B1
create_link sink1 B1

