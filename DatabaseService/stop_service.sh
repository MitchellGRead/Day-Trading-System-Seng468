#!/bin/bash

source $(dirname $0)/config.sh

cont=$db_service_name

echo 'Stopping database service...'
sudo docker stop $cont > /dev/null