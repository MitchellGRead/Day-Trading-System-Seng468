#!/bin/bash
curr_path=$(dirname $(realpath -e $0))
par_path=$(dirname $curr_path)

source $par_path/dbconfig.sh

cont_name=$mongo_db_name

# Tear down existing container if it exists
docker stop $cont_name
docker rm $cont_name
