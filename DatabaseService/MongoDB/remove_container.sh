#!/bin/bash
name=mongo-db
tag=4.4

# Tear down existing image and container if they exist
docker stop $name-$tag
docker rm $name-$tag