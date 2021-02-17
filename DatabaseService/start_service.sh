#!/bin/bash
curr_path=$(dirname $0)
source $curr_path/config.sh

image=$db_service_image
cont=$db_service_name

$curr_path/build_service.sh 2>/dev/null
echo 'Starting database service...'
sudo $curr_path/runDbContainers.sh
sudo docker rm $cont 2>&1 1>/dev/null
sudo docker run --name $cont -p 5656:5656 -it --network myNetwork -d $image > /dev/null