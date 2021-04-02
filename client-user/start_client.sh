#!/bin/bash

curr_path=$(dirname $0)
source $curr_path/config.sh

image=$client_image
cont=$client_name
port=$client_port

$curr_path/build_client.sh 2> /dev/null
echo 'Starting client...'
sudo docker rm $cont
sudo docker run -it --name $cont -p $port:$port $image