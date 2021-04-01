#!/bin/bash
curr_path=$(dirname $(realpath -e $0))
par_path=$(dirname $curr_path)

source $par_path/dbconfig.sh

img_name=$postgres_image_name
cont_name=$postgres_db_name

# Tear down existing image and container if they exist
a=$($curr_path/remove_container.sh 2>/dev/null)

# Build new container, exit if error encountered
sudo docker build -f $curr_path/Dockerfile -t $img_name $curr_path/docker_context
echo Built docker image titled $img_name
if 
    [ $? -eq 0 ]
then 
    sudo docker run --name $cont_name -p 5432:5432/tcp --cpuset-cpus="0,1" --network myNetwork -d $img_name
    echo Started docker container titled $cont_name
else
    exit 1
fi
