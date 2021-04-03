#!/bin/bash

curr_path=$(dirname $0)
source $curr_path/config.sh 

$curr_path/stop_client.sh 2> /dev/null

echo 'Building client...'
image=$client_image
sudo docker build -f $curr_path/Dockerfile -t $image $curr_path
