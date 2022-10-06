#!/bin/bash

target=$1
# B establish ovs
function dexec() {
	docker exec ${target:='B1'} $*
}
dexec ovs-vsctl --may-exist add-br br0
echo "created bridge:"
dexec ovs-vsctl list-br   
dexec ovs-vsctl --may-exist add-port br0 B1A1veth
dexec ovs-vsctl --may-exist add-port br0 B1AP1veth
dexec ovs-vsctl --may-exist add-port br0 B1C1veth
dexec ovs-vsctl --may-exist add-port br0 B1sink1veth
echo "br0 connected with port:"
dexec ovs-vsctl list-ports br0 
