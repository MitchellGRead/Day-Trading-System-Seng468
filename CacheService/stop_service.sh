#!/bin/bash

source $(dirname $0)/config.sh

cont=$cache_service_name

echo 'Stopping cache service...'
sudo docker stop $cont > /dev/null