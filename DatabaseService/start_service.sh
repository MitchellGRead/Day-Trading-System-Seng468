#!/bin/bash
curr_path=$(dirname $0)
source $curr_path/config.sh

image=$db_service_image
cont=$db_service_name
port=$db_service_port
network=$network_name

sudo $curr_path/runDbContainers.sh 2>/dev/null

sleep 3
$curr_path/build_service.sh 2>/dev/null
echo 'Starting database service...'
sudo docker rm $cont >/dev/null 2>&1
sudo docker run --name $cont -p $port:$port --network $network -d $image > /dev/null
