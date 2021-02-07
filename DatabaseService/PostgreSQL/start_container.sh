#!/bin/bash
name=trading-db
tag=13

# Tear down existing image and container if they exist
a=$(./remove_container.sh > /dev/null 2>&1)

# Build new container, exit if error encountered
docker build -f ./Dockerfile -t $name:$tag ./docker_context
echo Built docker image titled $name:$tag
if 
    [ $? -eq 0 ]
then 
    docker run --name $name-$tag -p 5432:5432/tcp -d $name:$tag
    echo Started docker container titled $name-$tag
else
    exit 1
    pause
fi