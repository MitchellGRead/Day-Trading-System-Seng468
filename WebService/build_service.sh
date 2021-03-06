#!/bin/bash

curr_path=$(dirname $0)
source $curr_path/config.sh

$curr_path/stop_service.sh 2>/dev/null

echo 'Building web service...'
image=$web_service_image
sudo docker build -f $curr_path/Dockerfile -t $image $curr_path/docker_context/ > /dev/null