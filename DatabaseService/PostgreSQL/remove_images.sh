#!/bin/bash
par_path=$(dirname $curr_path)
source $par_path/dbconfig.sh

img_name=$postgres_image_name
cont_name=$postgres_db_name

# Tear down existing image and container if they exist
sudo docker stop $cont_name
sudo docker rm $cont_name
sudo docker image rm $img_name
sudo docker image rm postgres:13