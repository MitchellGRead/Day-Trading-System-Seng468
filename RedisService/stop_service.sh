#!/bin/bash

source $(dirname $0)/config.sh

cont=$redis_service_name

echo 'Stopping redis service...'
sudo docker stop $cont > /dev/null