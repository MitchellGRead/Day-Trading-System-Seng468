#!/bin/bash
name=trading-db
tag=13

# Tear down existing image and container if they exist
a=$(docker stop $name-$tag > /dev/null 2>&1 &)
a=$(docker rm $name-$tag > /dev/null 2>&1 &)
a=$(docker image rm $name:$tag > /dev/null 2>&1 &)