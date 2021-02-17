#!/bin/bash

curr_path=$(dirname $0)
source $curr_path/config.sh

image=$trans_service_image
cont=$trans_service_name
port=$trans_service_port

$curr_path/build_service.sh 2>/dev/null
echo 'Starting transaction service...'
sudo docker rm $cont >/dev/null 2>&1
sudo docker run --name $cont -p $port:$port --network myNetwork -d $image > /dev/null