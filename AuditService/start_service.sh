#!/bin/bash

curr_path=$(dirname $0)
source $curr_path/config.sh

image=$audit_service_image
cont=$audit_service_name
port=$audit_service_port
network=$network_name

$curr_path/build_service.sh 2>/dev/null
echo 'Starting audit service...'
sudo docker rm $cont >/dev/null 2>&1
sudo docker run --name $cont -p $port:$port --cpuset-cpus="0" --network $network -d $image > /dev/null