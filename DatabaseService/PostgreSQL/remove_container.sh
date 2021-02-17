#!/bin/bash
par_path=$(dirname $curr_path)
source $par_path/dbconfig.sh

cont_name=$postgres_db_name

# Tear down existing container if they exist
sudo docker stop $cont_name
sudo docker rm $cont_name