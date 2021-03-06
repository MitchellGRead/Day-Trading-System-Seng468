#!/bin/bash
curr_path=$(dirname $(realpath -e $0))
par_path=$(dirname $curr_path)

source $par_path/dbconfig.sh

cont_name=$postgres_db_name

# Tear down existing container if it exists
sudo docker stop $cont_name
sudo docker rm $cont_name
