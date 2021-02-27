#!/bin/bash

curr_path=$(dirname $0)
source $curr_path/config.sh

image=$dummy_service_image
cont=$dummy_service_name
port=$dummy_service_port
network=$network_name

$curr_path/build_service.sh 2>/dev/null
echo 'Starting dummy stock service...'
sudo docker rm $cont >/dev/null 2>&1
sudo docker run --name $cont -p $port:$port --network $network -d $image > /dev/null