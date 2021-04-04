#!/bin/bash
curr_path=$(dirname $(realpath -e $0))
par_path=$(dirname $curr_path)

source $par_path/dbconfig.sh
source $par_path/config.sh

img_name=$mongo_image_name

# Tear down existing image if it exists
docker image rm $img_name
docker image rm mongo:4.4-bionic
