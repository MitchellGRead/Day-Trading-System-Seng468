#!/bin/bash
name=trading-db
tag=13

# Tear down existing image and container if they exist
docker stop $name-$tag
docker rm $name-$tag