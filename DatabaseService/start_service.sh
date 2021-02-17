#!/bin/bash
curr_path=$(dirname $0)
source $curr_path/config.sh

image=$db_service_image
cont=$db_service_name
port=$db_service_port

sudo $curr_path/runDbContainers.sh

$curr_path/build_service.sh 2>/dev/null
echo 'Starting database service...'
sudo docker rm $cont >/dev/null 2>&1
sudo docker run --name $cont -p $port:$port --network myNetwork -d $image > /dev/null