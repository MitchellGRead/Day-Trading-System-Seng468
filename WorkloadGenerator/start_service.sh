#!/bin/bash

curr_path=$(dirname $0)
source $curr_path/config.sh

image=$generator_image
cont=$generator_name
port=$generator_port
network=$network_name

$curr_path/build_service.sh 2>/dev/null
echo 'Starting generator...'
sudo docker rm $cont >/dev/null 2>&1
sudo docker run -it --name $cont -p $port:$port --network $network $image /bin/bash --cpuset-cpus="0"