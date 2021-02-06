#!/bin/bash

# Tear down existing image and container
a=$(docker stop trading-db-13)
a=$(docker rm trading-db-13)
a=$(docker image rm trading-db:13)

# Build new container, exit if error encountered
docker build -f ./Dockerfile -t trading-db:13 ./docker_context
if 
    [ $? -eq 0 ]
then 
    docker run --name trading-db-13 -p 5432:5432/tcp -d trading-db:13 -c max_connections=100
else
    exit 1
fi