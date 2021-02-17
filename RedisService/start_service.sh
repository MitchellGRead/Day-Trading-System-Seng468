#!/bin/bash

curr_path=$(dirname $0)
source $curr_path/config.sh

image=$redis_service_image
cont=$redis_service_name
port=$redis_service_port

$curr_path/build_service.sh 2>/dev/null
echo 'Starting redis service...'
sudo docker rm $cont >/dev/null 2>&1
sudo docker run --name $cont -p $port:$port --network myNetwork -d $image > /dev/null