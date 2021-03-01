#!/bin/bash

curr_path=$(dirname $0)
source $curr_path/config.sh

image=$trigger_service_image
cont=$trigger_service_name
port=$trigger_service_port
network=$network_name

$curr_path/build_service.sh 2>/dev/null
echo 'Starting trigger service...'
sudo docker rm $cont >/dev/null 2>&1
sudo docker run --name $cont -p $port:$port --network $network -d $image > /dev/null